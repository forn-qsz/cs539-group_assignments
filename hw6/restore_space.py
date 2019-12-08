from nlm import NLM
from math import log

if __name__ == "__main__":
    NLM.load("huge")

    x = "therestcanbeatotalmessandyoucanstillreaditwithoutaproblem"
    #x = "thisisbecausethehumanminddoesnotreadeveryletterbyitselfbutthewordasawhole"
    y = "the_rest_can_be_a_total_mess_and_you_can_still_read_it_without_a_problem"
    #y = "this_is_because_the_human_mind_does_not_read_every_letter_by_itself_but_the_word_as_a_whole"

    h = NLM()
    #p = 0
    beam = [(0, h)]
    b = 20
    for c in list(x) + ["</s>"]:
        newbeam = []
        for score, state in beam:
            newscore = score + log(state.next_prob(c))
            newstate = state + c
            newbeam.append((newscore, newstate))

            newscore = score + log(state.next_prob("_")) + log((state+"_").next_prob(c))
            newstate = state + '_' + c
            newbeam.append((newscore, newstate))

        beam = sorted(newbeam, reverse = True)[:b]

    score, state = beam[0]
    #print("".join(state.history[1:-1]).replace("_", " "))
    print(" ".join(state.history))
