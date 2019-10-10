# Libraries.
import nltk
from nltk.chunk import conlltags2tree, tree2conlltags
nltk.download('maxent_ne_chunker')
nltk.download('words')
from itertools import combinations

# Apply Named-Entity and Parts of speech tagging to extract features and also calculate Frequency.
def named_Entity(cluster):

    # Tokenize.
    text = nltk.word_tokenize(cluster)
    ne = nltk.ne_chunk(nltk.pos_tag(text)) # Create chunks.
    iob_tagged = tree2conlltags(ne)  # Apply NE.
    # print(iob_tagged)

    # List initializations.
    NNJJ = []
    nnp = []
    noun_add = []
    trigr = []
    NN = []
    NNP_Final = [] # Node with NNP.
    features_list_aj_nn = [] # For trigrams.
    features_list_nouns = [] # For total feature calculations.
    features_list_big1 = [] # For bi-grams of nouns.
    features_list_big2 = [] # for bi-grams of adjectives and nounpairs.
    feature_final = [] # Gives Final features.
    nouns_only = [] # When nothing is extracted, the nouns are extracted.

    # To retrieve nodes using NNP tags
    for j in range(0, len(iob_tagged)-1):
        if(iob_tagged[j][1] == 'NNP'):
            noun = iob_tagged[j]
            nnp .append(noun)

        if (iob_tagged[j][1] == 'NN'):
            noun1 = iob_tagged[j]
            NN.append(noun1)

    # To retrieve adjectives and Nouns in the sentences
    for i in range(0, len(iob_tagged) - 1):
        if (iob_tagged[i][1] == 'JJ' and iob_tagged[i + 1][1] == 'NN'):
            w = iob_tagged[i] + iob_tagged[i+1]
            NNJJ.append(w)

        if(iob_tagged[i][1] == 'NN' and iob_tagged[i + 1][1] == 'NN'):
            nnnn = iob_tagged[i] + iob_tagged[i + 1]
            noun_add.append(nnnn)

        if(iob_tagged[i][1] == 'JJ' and iob_tagged[i + 1][1] == 'NN' and iob_tagged[i + 2][1] == 'NN' ):
            trigram = iob_tagged[i] + iob_tagged[i + 1] + iob_tagged[i + 2]
            trigr.append(trigram)

    # Calculate Frequency
    # For NNP.
    fre_nnp = nltk.FreqDist(nnp)
    for word, frequency in fre_nnp.most_common(15):
        print(word[0],'is a proper noun having a frequency of:',frequency)
        NNP_Final.append(word[0])

    # For Adjectives:Nouns:Nouns.
    fre_trinn = nltk.FreqDist(trigr)
    for word, frequency in fre_trinn.most_common(15):
        aj_nn = (word[0] +' '+ word[3] +' ' + word[6])
        features_list_aj_nn.append(aj_nn)
    print('Feature_Set_trigrams:',features_list_aj_nn)

    # For Nouns.
    fre_noun = nltk.FreqDist(noun_add)
    for word, frequency in fre_noun.most_common(15):
        for_nouns = (word[0] + ' ' + word[3])
        features_list_nouns.append(for_nouns)
        features_list_big1.append(for_nouns)
    print('Feature_Set_bigrams_1:',features_list_big1)

    # For adjectives and Nouns
    fre_nnjj = nltk.FreqDist(NNJJ)
    for word, frequency in fre_nnjj.most_common(15):
        for_bigram2 = (word[0] + ' ' + word[3])
        if(for_bigram2 not in features_list_nouns):
            features_list_nouns.append(for_bigram2)
        features_list_big2.append(for_bigram2)
    print('Feature_Set_bigrams_2:', features_list_big2)


    # Checks which features to keep and which to discard.
    for i in features_list_aj_nn:
        for j in features_list_nouns:
            if j in i and i not in feature_final:
                feature_final.append(i)
                features_list_nouns.remove(j)

    # Handled an Exception - Code could have been improvised.
    for i in features_list_aj_nn:
        for j in features_list_nouns:
            if j in i and i in feature_final:
                features_list_nouns.remove(j)

    # Complete set of features.
    complete_set = (feature_final + features_list_nouns)
    print('Total Feature set:',complete_set)

    # If the complete list contains unstructured keywords which needs processing.
    # Here the variable is hardcoded.
    for e in complete_set:
        if 'anti-trap protection' in e:
            complete_set.remove(e)

    # For Noun pairs extraction when nothing else is extracted.
    list1 = []
    if (len(complete_set) == 0):
        fre_onlynn = nltk.FreqDist(NN)

        # Checks for frequency criteria.
        for word, frequency in fre_onlynn.most_common(15):
            list1.append(frequency)
        criteria = max(list1)

        # Selects only valid features which match the criteria.
        for word, frequency in fre_onlynn.most_common(15):
            if(frequency>=int(criteria/2)):
                nouns_only.append(word[0])
        print('Feature set extended:',nouns_only)

        for elements in list(combinations(nouns_only, 2)):
            for i in elements:
                andor.append(i.split())
        print('The combinations to find andor:', andor)

    # # To Find AND and OR.
    for elements in list(combinations(complete_set, 2)):
        for i in elements:
            andor.append(i.split())
    print('The combinations to find andor:',andor)

