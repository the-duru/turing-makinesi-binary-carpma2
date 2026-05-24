"""
Final Ödev 2: Turing Makinesi ile Araç Plaka Formatı Tanıyıcı
Tanınan dil: NNLLNNN (2 rakam, 2 büyük harf, 3 rakam)
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


BLANK = "_"


class SymbolKind(Enum):
    DIGIT = "DIGIT"
    UPPER = "UPPER"
    BLANK = "BLANK"
    OTHER = "OTHER"


def classify(symbol: str) -> SymbolKind:
    if symbol == BLANK:
        return SymbolKind.BLANK
    if len(symbol) == 1 and symbol.isdigit():
        return SymbolKind.DIGIT
    if len(symbol) == 1 and "A" <= symbol <= "Z":
        return SymbolKind.UPPER
    return SymbolKind.OTHER


@dataclass(frozen=True)
class Transition:
    next_state: str
    write_symbol: str
    move: str  # R, L, S


# Geçiş fonksiyonu: (durum, sembol türü) -> Transition
# Doğrulama mantığı yalnızca bu tabloda; if-else ile format kontrolü yapılmaz.
TRANSITION_TABLE: dict[tuple[str, SymbolKind], Transition] = {
    ("q0", SymbolKind.DIGIT): Transition("q1", "", "R"),
    ("q0", SymbolKind.UPPER): Transition("q_red", "", "R"),
    ("q0", SymbolKind.OTHER): Transition("q_red", "", "R"),
    ("q0", SymbolKind.BLANK): Transition("q_red", "", "R"),
    ("q1", SymbolKind.DIGIT): Transition("q2", "", "R"),
    ("q1", SymbolKind.UPPER): Transition("q_red", "", "R"),
    ("q1", SymbolKind.OTHER): Transition("q_red", "", "R"),
    ("q1", SymbolKind.BLANK): Transition("q_red", "", "R"),
    ("q2", SymbolKind.DIGIT): Transition("q_red", "", "R"),
    ("q2", SymbolKind.UPPER): Transition("q3", "", "R"),
    ("q2", SymbolKind.OTHER): Transition("q_red", "", "R"),
    ("q2", SymbolKind.BLANK): Transition("q_red", "", "R"),
    ("q3", SymbolKind.DIGIT): Transition("q_red", "", "R"),
    ("q3", SymbolKind.UPPER): Transition("q4", "", "R"),
    ("q3", SymbolKind.OTHER): Transition("q_red", "", "R"),
    ("q3", SymbolKind.BLANK): Transition("q_red", "", "R"),
    ("q4", SymbolKind.DIGIT): Transition("q5", "", "R"),
    ("q4", SymbolKind.UPPER): Transition("q_red", "", "R"),
    ("q4", SymbolKind.OTHER): Transition("q_red", "", "R"),
    ("q4", SymbolKind.BLANK): Transition("q_red", "", "R"),
    ("q5", SymbolKind.DIGIT): Transition("q6", "", "R"),
    ("q5", SymbolKind.UPPER): Transition("q_red", "", "R"),
    ("q5", SymbolKind.OTHER): Transition("q_red", "", "R"),
    ("q5", SymbolKind.BLANK): Transition("q_red", "", "R"),
    ("q6", SymbolKind.DIGIT): Transition("q7", "", "R"),
    ("q6", SymbolKind.UPPER): Transition("q_red", "", "R"),
    ("q6", SymbolKind.OTHER): Transition("q_red", "", "R"),
    ("q6", SymbolKind.BLANK): Transition("q_red", "", "R"),
    ("q7", SymbolKind.BLANK): Transition("q_accept", "", "S"),
    ("q7", SymbolKind.DIGIT): Transition("q_red", "", "R"),
    ("q7", SymbolKind.UPPER): Transition("q_red", "", "R"),
    ("q7", SymbolKind.OTHER): Transition("q_red", "", "R"),
}


STATES = {
    "q0",
    "q1",
    "q2",
    "q3",
    "q4",
    "q5",
    "q6",
    "q7",
    "q_accept",
    "q_red",
}
START_STATE = "q0"
ACCEPT_STATE = "q_accept"
REJECT_STATE = "q_red"
INPUT_ALPHABET = set("0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ")
TAPE_ALPHABET = INPUT_ALPHABET | {BLANK}


@dataclass
class StepLog:
    step: int
    state: str
    symbol: str
    move: str
    tape: str
    head_index: int


class TuringMachine:
    def __init__(self, input_string: str) -> None:
        self.input_string = input_string
        self.tape: list[str] = [BLANK] + list(input_string) + [BLANK]
        self.head = 1
        self.state = START_STATE
        self.step = 0
        self.logs: list[StepLog] = []
        self.halted = False
        self.result: str | None = None

    def tape_display(self) -> str:
        parts: list[str] = []
        for i, cell in enumerate(self.tape):
            ch = cell if cell != BLANK else "□"
            if i == self.head:
                parts.append(f"[{ch}]")
            else:
                parts.append(ch)
        return "".join(parts)

    def read_symbol(self) -> str:
        if self.head < 0:
            self.tape.insert(0, BLANK)
            self.head = 0
        if self.head >= len(self.tape):
            self.tape.append(BLANK)
        return self.tape[self.head]

    def move_head(self, direction: str) -> None:
        if direction == "R":
            self.head += 1
        elif direction == "L":
            self.head -= 1

    def log_step(self, symbol: str, move: str) -> None:
        self.logs.append(
            StepLog(
                step=self.step,
                state=self.state,
                symbol=symbol if symbol != BLANK else "boşluk",
                move=move,
                tape=self.tape_display(),
                head_index=self.head,
            )
        )

    def step_once(self) -> bool:
        """Tek adım çalıştırır. Durduysa False döner."""
        if self.halted:
            return False

        if self.state == ACCEPT_STATE:
            self.result = "KABUL"
            self.halted = True
            return False

        if self.state == REJECT_STATE:
            self.result = "RED"
            self.halted = True
            return False

        raw = self.read_symbol()
        kind = classify(raw)
        key = (self.state, kind)
        transition = TRANSITION_TABLE.get(key)

        if transition is None:
            self.state = REJECT_STATE
            self.log_step(raw, "→ RED")
            self.result = "RED"
            self.halted = True
            return False

        move = transition.move
        self.log_step(raw, move if move != "S" else "dur")

        self.state = transition.next_state

        if transition.write_symbol:
            self.tape[self.head] = transition.write_symbol

        if self.state == ACCEPT_STATE:
            self.result = "KABUL"
            self.halted = True
            return False

        if self.state == REJECT_STATE:
            self.result = "RED"
            self.halted = True
            return False

        if move in ("R", "L"):
            self.move_head(move)

        self.step += 1
        return True

    def run(self, verbose: bool = True) -> str:
        if verbose:
            print(f"\nGirdi bandı: {self.input_string!r}")
            print(f"Başlangıç durumu: {START_STATE}")
            print("-" * 60)

        while self.step_once():
            if verbose and self.logs:
                last = self.logs[-1]
                print(
                    f"Adım {last.step:2d} | Durum: {last.state:8s} | "
                    f"Okunan: {last.symbol:6s} | Hareket: {last.move:4s} | "
                    f"Bant: {last.tape}"
                )

        if verbose:
            print("-" * 60)
            if self.logs:
                last = self.logs[-1]
                print(
                    f"Son adım | Durum: {self.state:8s} | "
                    f"Okunan: {last.symbol:6s} | Sonuç: {self.result}"
                )
            print(f"\n>>> {self.result} <<<\n")

        return self.result or "RED"


def run_plate_checker(plate: str, verbose: bool = True) -> str:
    tm = TuringMachine(plate)
    return tm.run(verbose=verbose)


def run_test_suite(verbose: bool = False) -> None:
    valid = ["55AB123", "34TR456", "06AA789", "00ZZ000", "99XY999"]
    invalid = [
        "5AB123",    # eksik rakam
        "555AB12",   # fazla karakter
        "34A1234",   # harf eksik
        "AB34123",   # rakamla başlamıyor
        "34AB12X",   # geçersiz sembol
        "55ab123",   # küçük harf
    ]

    print("=" * 60)
    print("TEST PAKETİ — Geçerli girdiler (beklenen: KABUL)")
    print("=" * 60)
    for plate in valid:
        result = run_plate_checker(plate, verbose=verbose)
        status = "OK" if result == "KABUL" else "HATA"
        print(f"  [{status}] {plate!r} -> {result}")

    print("\n" + "=" * 60)
    print("TEST PAKETİ — Geçersiz girdiler (beklenen: RED)")
    print("=" * 60)
    for plate in invalid:
        result = run_plate_checker(plate, verbose=verbose)
        status = "OK" if result == "RED" else "HATA"
        print(f"  [{status}] {plate!r} -> {result}")


def main() -> None:
    print("Turing Makinesi — Araç Plaka Formatı Tanıyıcı (NNLLNNN)")
    print("Çıkmak için boş Enter, test paketi için 't' yazın.\n")

    while True:
        plate = input("Plaka girin: ").strip()
        if not plate:
            print("Program sonlandı.")
            break
        if plate.lower() == "t":
            run_test_suite(verbose=False)
            continue
        run_plate_checker(plate, verbose=True)


if __name__ == "__main__":
    main()
