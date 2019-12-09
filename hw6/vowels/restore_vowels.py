from nlm import NLM
from math import log

if __name__ == "__main__":
    NLM.load("large")

    
    x = "yt_dmnstrtn_ffcls_hv_bgn_t_dscrb_clmb_s_nthr_grv_strtgc_rsk"
    y = "yet_administration_officials_have_begun_to_describe_colombia_as_another_grave_strategic_risk"


    VOWELS = ['a', 'e', 'i', 'o', 'u']
    MAX_REPEAT = 2
    h = NLM()
    #p = 0
    beam = [(0, h)]
    b = 40
    for c in list(x) + ["</s>"]:
        newbeam = []
        prev = [beam]
        for i in range(MAX_REPEAT+1):
            tmp = []
            for score, state in prev[-1]:
                newscore = score + log(state.next_prob(c))
                newstate = state + c
                newbeam.append((newscore, newstate))
                if i <= MAX_REPEAT:
                    for vowel in VOWELS:
                        newscore = score + log(state.next_prob(vowel))
                        newstate = state + vowel
                        tmp.append((newscore, newstate))
            prev.append(tmp)

        beam = sorted(newbeam, reverse = True, key = lambda x : x[0])[:b]

    score, state = beam[0]
    #print("".join(state.history[1:-1]).replace("_", " "))
    print(" ".join(state.history))
