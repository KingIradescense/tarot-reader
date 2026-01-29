#draw_cards.py

from __future__ import annotations

import random
from typing import List, Tuple, Dict, Optional
from dataclasses import dataclass

CardTuple = Tuple[int, str, str, str] # (number/PID, name,  upright meaning, reversed meaning)
ReadingItem = Dict[str, object] # generic dict for readings
CardDraw = Tuple[int, int]  # (card PID, orientation 0=upright, 1=reversed)
Spread = Tuple[int, int, str, str] # (PID, number of cards, name, description)

#arcana cards
#? major cards currently implemented
#! TODO: add minor arcana cards

cards: List[CardTuple] = [
    (0, "The Fool","New beginnings, optimism, trust in life", "Recklessness, foolishness, naivete"),
    (1, "The Magician", "Focus, willpower, making things real", "Manipulation, poor planning, untapped talents"),
    (2, "The High Priestess", "Intuition, sacred knowledge, divine feminine", "Secrets, disconnected from intuition, withdrawal and silence"),
    (3, "The Empress", "Femininity, beauty, nature, nurturing, abundance", "Creative block, dependence on others"),
    (4, "The Emperor", "Authority, establishment, structure, a father figure","Domination, excessive control, lack of discipline, inflexibility"),
    (5, "The Hierophant", "Spiritual wisdom, religious beliefs, conformity, tradition, institutions","Personal beliefs, freedom, challenging the status quo"),
    (6, "The Lovers", "Love, harmony, relationships, values alignment, choices","Self-love, disharmony, imbalance, misalignment of values"),
    (7, "The Chariot", "Control, willpower, success, action, determination","Self-discipline, opposition, lack of direction"),
    (8, "Strength", "Strength, courage, persuasion, influence, compassion","Inner strength, self-doubt, low energy, raw emotion"),
    (9, "The Hermit", "Soul-searching, introspection, being alone, inner guidance","Isolation, loneliness, withdrawal"),
    (10, "Wheel of Fortune", "Good luck, karma, life cycles, destiny, a turning point","Bad luck, resistance to change, breaking cycles"),
    (11, "Justice", "Justice, fairness, truth, cause and effect, law","Unfairness, lack of accountability, dishonesty"),
    (12, "The Hanged Man", "Pause, surrender, letting go, new perspectives","Delays, resistance, stalling, indecision"),
    (13, "Death", "Endings, change, transformation, transition","Fear of change, holding on, stagnation")
]

# types of spreads

spreads: List[Spread] = [
    (0, 1, "Daily Card", "A single card to provide insight for the day ahead."),
    (1, 1, "Yes/No", "A single card to answer a yes or no question."),
    (2, 1, "Advice", "A single card offering guidance or advice."),
    (3, 2, "Situation and Advice", "Two cards: one representing the current situation and the other offering advice."),
    (4, 2, "You and Them", "Two cards: one for you and one for another person involved."),
    (5, 2, "One or the Other", "Two cards representing two different options or paths."),
    (6, 3, "Past, Present, Future", "Three cards representing the past, present, and future of a situation."),
    (7, 3, "Mind, Body, Spirit", "Three cards representing the mental, physical, and spiritual aspects of a situation."),
    (8, 3, "Situation, Obstacle, Advice", "Three cards representing the current situation, recommended action, and potential outcome."),
    (9, 3, "Strength, Weakness, Guidance", "Three cards representing strengths, weaknesses, and guidance."),
    (10, 3, "You, Them, Relationship", "Three cards representing you, another person, and the relationship between you."),
    (11, 3, "Stop, Start, Continue", "Three cards representing what to stop, start, and continue doing."),
    (12, 4, "Cross", "Four cards representing the situation, challenge, advice, and outcome."),
    (13, 5, "Decision", "Five cards representing the situation, options, advice, potential outcome, and final outcome."),
    (14, 5, "Goals", "Five cards representing current state, desired state, obstacles, resources, and next steps."),
    (15, 7, "Horseshoe", "Seven cards representing past influences, present situation, hidden influences, obstacles, attitudes, external influences, and outcome."),
    (16, 7, "Relationship", "Seven cards representing you, them, the relationship, strengths, weaknesses, advice, and outcome."),
    (17, 9, "3x3", "Nine cards laid out in a 3x3 grid; a more indepth version of the 3-card spreads."),
    (18, 10, "Celtic Cross", "Ten cards representing the present, challenge, past, future, above, below, advice, external influences, hopes and fears, and outcome.")
]

#! TODO: define COMBINED READINGS structure; refers to prewritten unique reading results
# COMBINED READINGS = Dict[...]

def _norm(name: str) -> str:
    """
    normalizes a spread name for comparison
    lowercases, spaces, non-alphanumeric chars removed
    """
    return "".join(ch for ch in name.lower().strip() if ch.isalnum())

@dataclass(slots = True)
class DrawCards:
    """
    minimal dispatcher for tarot spreads
    takes the number of cards and the spread name, uses it to route
    to a spread-specific action via match/case
    #! action bodies currently not complete (168)
    """

    n_cards: int
    spread_name: str
    def __post_init__(self) -> None:
        if not isinstance(self.n_cards, int) or self.n_cards < 1:
            raise ValueError("n_cards must be a positive integer")
        if not isinstance(self.spread_name, str) or not self.spread_name:
            raise ValueError("spread_name must be a non-empty string")
        
    def dispatch(self) -> None:

        """
        chooses what to do based on spread name and number of cards
        checks by number of cards first, then spread name
        """

        match self.n_cards:
            case 1:
                match _norm(self.spread_name):
                    case "dailycard":
                        self._action_daily()
                    case "yes/no":
                        self._action_yes_no()
                    case "advice":
                        self._action_advice()
                    case _:
                        raise ValueError(f"Unknown 1-card spread: {self.spread_name}")
            case 2:
                match _norm(self.spread_name):
                    case "situationandadvice":
                        self._action_situation_and_advice()
                    case "youandthem":
                        self._action_you_and_them()
                    case "oneortheother":
                        self._action_one_or_the_other()
                    case _:
                        raise ValueError(f"Unknown 2-card spread: {self.spread_name}")
            case 3:
                match _norm(self.spread_name):
                    case "pastpresentfuture":
                        self._action_past_present_future()
                    case "mindbodyspirit":
                        self._action_mind_body_spirit()
                    case "situationobstacleadvice":
                        self._action_situation_obstacle_advice()
                    case "strengthweaknessguidance":
                        self._action_strength_weakness_guidance()
                    case "youthemrelationship":
                        self._action_you_them_relationship()
                    case "stopstartcontinue":
                        self._action_stop_start_continue()
                    case _:
                        raise ValueError(f"Unknown 3-card spread: {self.spread_name}")
            case 4:
                match _norm(self.spread_name):
                    case "cross":
                        self._action_cross()
                    case _:
                        raise ValueError(f"Unknown 4-card spread: {self.spread_name}")
            case 5:
                match _norm(self.spread_name):
                    case "decision":
                        self._action_decision()
                    case "goals":
                        self._action_goals()
                    case _:
                        raise ValueError(f"Unknown 5-card spread: {self.spread_name}")
            case 7:
                match _norm(self.spread_name):
                    case "horseshoe":
                        self._action_horseshoe()
                    case "relationship":
                        self._action_relationship_7()
                    case _:
                        raise ValueError(f"Unknown 7-card spread: {self.spread_name}")
            case 9:
                match _norm(self.spread_name):
                    case "3x3":
                        self._action_3x3()
                    case _:
                        raise ValueError(f"Unknown 9-card spread: {self.spread_name}")
            case 10:
                match _norm(self.spread_name):
                    case "celticcross":
                        self._action_celtic_cross()
                    case _:
                        raise ValueError(f"Unknown 10-card spread: {self.spread_name}")
            case _:
                raise ValueError(f"No spreads available for {self.n_cards} cards")        
            

#! TODO: finish action stubs
    # stubs for actions

    def _action_daily(self) -> None: 
        drawn = self.shuffle_deck() 
        print_spread_reading(
            position_labels = ["Daily Card"],
            drawn = drawn,
            cards = cards,
        )
    def _action_yes_no(self) -> None: raise NotImplementedError
    def _action_advice(self) -> None: raise NotImplementedError

    def _action_situation_and_advice(self) -> None: raise NotImplementedError
    def _action_you_and_them(self) -> None: raise NotImplementedError
    def _action_one_or_the_other(self) -> None: raise NotImplementedError

    def _action_past_present_future(self) -> None:
        drawn = self.shuffle_deck()
        print_spread_reading(
            position_labels = ["Past", "Present", "Future"],
            drawn = drawn,
            cards = cards,
        )
    def _action_mind_body_spirit(self) -> None: raise NotImplementedError
    def _action_situation_obstacle_advice(self) -> None: raise NotImplementedError
    def _action_strength_weakness_guidance(self) -> None: raise NotImplementedError
    def _action_you_them_relationship(self) -> None: raise NotImplementedError
    def _action_stop_start_continue(self) -> None: raise NotImplementedError

    def _action_cross(self) -> None: raise NotImplementedError
    def _action_decision(self) -> None: raise NotImplementedError
    def _action_goals(self) -> None: raise NotImplementedError

    def _action_horseshoe(self) -> None: raise NotImplementedError
    def _action_relationship_7(self) -> None: raise NotImplementedError

    def _action_3x3(self) -> None: raise NotImplementedError
    def _action_celtic_cross(self) -> None: raise NotImplementedError 

    def shuffle_deck(
            self,
            *,
            seed: Optional[int] = None,
            shuffle_order: bool = True,
    ) -> List[CardDraw]:
        """
        returns a shuffled deck of tarot cards
        optional seed for reproducibility
        optional shuffle_order to skip shuffling (for testing)
        """

        rng = random.Random(seed)

        deck_ids = list(range(len(cards)))
        orientation = [0] * len(cards)

        reversed_ids = rng.sample(deck_ids, k=len(cards)//2) # half the cards are randomly reversed
        for pid in reversed_ids:
            orientation[pid] = 1

        deck: List[CardDraw] = [(pid, orientation[pid]) for pid in deck_ids]

        if shuffle_order:
            rng.shuffle(deck)

        drawn = deck[: self.n_cards]

        return drawn



def print_spread_reading(
            *,
            position_labels: List[str],
            drawn: List[CardDraw],
            cards: List[CardTuple],
    ) -> None:
        
        """
        prints per-card results in drawn order with position labels
        """
    
        for label, (pid, bit) in zip(position_labels, drawn):
            _, name, upright, reversed_ = _card_by_pid(cards, pid)
            meaning = upright if bit == 0 else reversed_
            shown_name = name if bit == 0 else f"Reversed {name}"

            #? prints tuple for verification. Remove later.
            print(f" {label}: {pid, bit} -> {shown_name} -> {meaning}")

        print()
        print("[combined reading placeholder]")

def _card_by_pid(cards: List[CardTuple], pid: int) -> CardTuple:
        """
        returns the card tuple for the given PID from CardDraw in drawn
        raises ValueError if PID not found
        """
        for card in cards:
            if card[0] == pid:
                return card
        raise ValueError(f"Card with PID {pid} not found")




if __name__ == "__main__":
    DrawCards(n_cards=3, spread_name="Past, Present, Future").dispatch()
