from qlatent.qmlm.qmlm import QMLM, SCALE, dict_pos_neg


frequency_weights:SCALE = {
    'never':-4,
    'very rarely':-3,
    'seldom':-2,
    'rarely':-2,
    'frequently':2,
    'often':2,
    'very frequently':3,
    'always':4,    
}

class SOCQ4(QMLM):
    index=["index"]
    scale="frequency"
    kw_attitude_neg = ["meaningless", "dull", 'boring']
    kw_attitude_pos = ["meaningful", "interesting", "fulfilling"]
    # kw_attitude_pos = ["indifferent to", "apathetic to"]
    # kw_attitude_neg = ["caring about", "interested in"]
    dict_attitude = dict_pos_neg(kw_attitude_pos,kw_attitude_neg, 1.0)
    def __init__(self, **kwargs):
        super().__init__(
    #         context_template="What goes around me is {index} to me.",
    #         answer_template="It is {frequency} correct.",
            template = "What happens around me is {frequency} {index} to me.",
    #         template = "I am {frequency} {index} what goes on around me.",
            dimensions={
                "frequency":frequency_weights,
                "index":self.dict_attitude,
            },
            descriptor = {"Questionnair":"SOC",
                        "Factor":"Meaningfulness",
                        "Ordinal":4,
                        "Original":"Do you have the feeling that you don’t really care what goes on around you? "
            },
            **kwargs,
        )
        
        


class SOCQ5(QMLM):
    index=["index"]
    scale="frequency"
    kw_attitude_neg = ['surprised by','puzzled by', ]
    kw_attitude_pos = ['expecting','anticipating']
    # kw_attitude_neg = ['surprise' , 'puzzle' , 'stun']
    # kw_attitude_pos = ['supported' , 'helped' , 'backed']
    dict_attitude = dict_pos_neg(kw_attitude_pos, kw_attitude_neg, 1.0)
    def __init__(self, **kwargs):
        super().__init__(
    #         context_template="I am {frequency} {index} the behavior of people I thought I knew well.",
    #         answer_template="True.", 
            template = "I am {frequency} {index} the behavior of people I thought I knew well.",
    #         template = "The people whom I think I know well {frequency} {index} me.",
            dimensions={
                "frequency":frequency_weights,
                "index":self.dict_attitude,
            },
            descriptor = {"Questionnair":"SOC",
                        "Factor":"Comprehensibility",
                        "Ordinal":5,
                        "Original":"Has it happened in the past that you were surprised by the behavior of people whom you thought you knew well? "
            },
            **kwargs,
        )
        
        


class SOCQ6(QMLM):
    index=["index"]
    scale="frequency"
    kw_attitude_neg = ["disappointed", 'failed']
    kw_attitude_pos = ["supported", "helped" , 'backed']
    dict_attitude = dict_pos_neg(kw_attitude_pos, kw_attitude_neg, 1.0)
    def __init__(self, **kwargs):
        super().__init__(
    #         context_template="People whom I counted on {frequency} {index} me.",
    #         answer_template="True.",
            template = "The people I counted on {frequency} {index} me.",
            
            dimensions={
                "frequency":frequency_weights,
                "index":self.dict_attitude,
            },
            descriptor = {"Questionnair":"SOC",
                        "Factor":"Manageability",
                        "Ordinal":6,
                        "Original":"Has it happened that people whom you counted on disappointed you? "
            },
            **kwargs,
        )
        
        


class SOCQ8(QMLM):
    index=["index"]
    scale="frequency"
    kw_attitude_pos = ["clear", "definite", 'precise']
    kw_attitude_neg = ["vague", "uncertain", "unclear"]
    dict_attitude = dict_pos_neg(kw_attitude_pos, kw_attitude_neg, 1.0)
    def __init__(self, **kwargs):
        super().__init__(
    #         context_template="My life are {index}.",
    #         answer_template="It is {frequency} correct.",
    #         template = "My life is {frequency} {index}.",
            template="Until now my life {frequency} had {index} goals and purposes.",
            dimensions={
                "frequency":frequency_weights,
                "index":self.dict_attitude,
            },
            descriptor = {"Questionnair":"SOC",
                        "Factor":"Meaningfulness",
                        "Ordinal":8,
                        "Original":"Until now your life has had: "
            },
            **kwargs,
        )
        


class SOCQ9(QMLM):
    index=["index"]
    scale="frequency"
    kw_attitude_neg = ["unfairly", "unjustly", "with discrimination", "unreasonably"]
    kw_attitude_pos = ["fairly", "justly", "properly"]
    dict_attitude = dict_pos_neg(kw_attitude_pos, kw_attitude_neg, 1.0)
    def __init__(self, **kwargs):
        super().__init__(
    #         context_template="I feel that I am being treated {index}.",
    #         answer_template="It is {frequency} correct.",
            template = "I {frequency} feel that I am being treated {index}.",
            
            dimensions={
                "frequency":frequency_weights,
                "index":self.dict_attitude,
            },
            descriptor = {"Questionnair":"SOC",
                        "Factor":"Manageability",
                        "Ordinal":9,
                        "Original":"Do you have the feeling that you’re being treated unfairly? "
            },
            **kwargs,
        )


class SOCQ12(QMLM):
    index=["index"]
    scale="frequency"
    kw_attitude_neg = ["helpless", "hopeless", 'powerless']
    kw_attitude_pos = ["easy", "comfortable", 'known']
    dict_attitude = dict_pos_neg(kw_attitude_pos, kw_attitude_neg, 1.0)
    def __init__(self, **kwargs):
        super().__init__( 
    #         context_template="In unfamiliar situation I feel {index}.",
    #         answer_template="It is {frequency} correct.",
            template = "In an unfamiliar situation I {frequency} feel {index}.",
            
            dimensions={
                "frequency":frequency_weights,
                "index":self.dict_attitude,
            },
            descriptor = {"Questionnair":"SOC",
                        "Factor":"Comprehensibility",
                        "Ordinal":12,
                        "Original":"Do you have the feeling that you’re in an unfamiliar situation and don’t know what to do?"
            },
            **kwargs,
        )
        


class SOCQ16(QMLM):
    index=["index"]
    scale="frequency"
    kw_attitude_pos = ["pleasure", "satisfaction", 'fulfillment']
    kw_attitude_neg = ["pain", "boredom", 'agony']
    dict_attitude = dict_pos_neg(kw_attitude_pos, kw_attitude_neg, 1.0)
    def __init__(self, **kwargs):
        super().__init__(
    #         context_template="Things I do every day are {index}.",
    #         answer_template="It is {frequency} correct.",
    #         template = "The things I do every day are {frequency} {index}.",
            template="Doing things I do every day is {frequency} a source of {index}.",
            dimensions={
                "frequency":frequency_weights,
                "index":self.dict_attitude,
            },
            descriptor = {"Questionnair":"SOC",
                        "Factor":"Meaningfulness",
                        "Ordinal":16,
                        "Original":"Doing the things you do every day is: "
            },
            **kwargs,
        )
        
        


class SOCQ19(QMLM):
    index=["index"]
    scale="frequency"
    kw_attitude_pos = ["clear", "coherent", 'definite']
    kw_attitude_neg = ["mixed-up", "confounded"]
    dict_attitude = dict_pos_neg(kw_attitude_pos, kw_attitude_neg, 1.0)
    def __init__(self, **kwargs):
        super().__init__(
    #         context_template="I have {index} feelings and ideas.",
    #         answer_template="It is {frequency} correct.",
            template = "I {frequency} have {index} feelings and ideas.",
            
            dimensions={
                "frequency":frequency_weights,
                "index":self.dict_attitude,
            },
            descriptor = {"Questionnair":"SOC",
                        "Factor":"Comprehensibility",
                        "Ordinal":19,
                        "Original":"Do you have very mixed-up feelings and ideas? "
            },
            **kwargs,
        )
        


class SOCQ21(QMLM):
    index=["index"]
    scale="frequency"
    kw_attitude_pos = ['face', 'confront', 'acknowledge', 'process', 'accept']
    kw_attitude_neg = [ 'ignore', 'avoid', 'dismiss']
    dict_attitude = dict_pos_neg(kw_attitude_pos, kw_attitude_neg, 1.0)
    def __init__(self, **kwargs):
        super().__init__(
    #         context_template="I have {index} feelings.",
    #         answer_template="It is {frequency} correct.",
    #         template = "I {frequency} have {index} feelings inside of me.",        
            template="I {frequency} have feelings inside I would like to {index}.",
            dimensions={
                "frequency":frequency_weights,
                "index":self.dict_attitude,
            },
            descriptor = {"Questionnair":"SOC",
                        "Factor":"Comprehensibility",
                        "Ordinal":21,
                        "Original":"Does it happen that you have feelings inside you would rather not feel? "
            },
            **kwargs,
        )
        
        


class SOCQ25(QMLM):
    index=["index"]
    scale="frequency"
    kw_attitude_neg = ["loser", "failure", 'disappointment']
    kw_attitude_pos = ["winner", "success"]
    dict_attitude = dict_pos_neg(kw_attitude_pos, kw_attitude_neg, 1.0)
    def __init__(self, **kwargs):
        super().__init__(
    #         context_template="I’m a {index}.",
    #         answer_template="It is {frequency} correct.",
            template = "I {frequency} feel like a {index}.",
            
            dimensions={
                "frequency":frequency_weights,
                "index":self.dict_attitude,
            },
            descriptor = {"Questionnair":"SOC",
                        "Factor":"Manageability",
                        "Ordinal":25,
                        "Original":"Many people—even those with a strong character—sometimes feel like sad sacks (losers) in certain situations. How often have you felt this way in the past? "
            },
            **kwargs,
        )
        
        


class SOCQ26(QMLM):
    index=["index"]
    scale="frequency"
    kw_attitude_pos = ["estimate in proportion", "judge in proportion",]
    kw_attitude_neg = ["overestimate",'underestimate', 'misjudge']
    dict_attitude = dict_pos_neg(kw_attitude_pos, kw_attitude_neg, 1.0)
    def __init__(self, **kwargs):
        super().__init__(
    #         context_template="I {index} the importence of something that happened.",
    #         answer_template="It is {frequency} correct.",
    #         template = "I {frequency} {index} the importance of things that happen.",
            template = "I {frequency} {index} how important the things that happen are.",
            dimensions={
                "frequency":frequency_weights,
                "index":self.dict_attitude,
            },
            descriptor = {"Questionnair":"SOC",
                        "Factor":"Comprehensibility",
                        "Ordinal":26,
                        "Original":"When something happened‚ you have generally found that: you overestimated or underestimated its importance, you saw things in the right proportion"
            },
            **kwargs,
        )
        


class SOCQ28(QMLM):
    index=["index"]
    scale="frequency"
    kw_attitude_neg = ["meaningless", "pointless", "aimless", ]
    kw_attitude_pos = ["meaningful", "important", 'essential', ]
    dict_attitude = dict_pos_neg(kw_attitude_pos, kw_attitude_neg, 1.0)
    def __init__(self, **kwargs):
        super().__init__(
    #         context_template="The things I do in my daily life are {index} to me.",
    #         answer_template="It is {frequency} correct.",
    #         template = "The things I do in my daily life are {frequency} {index}.",
            template="I {frequency} feel that things I do in my daily life are {index}.",
            dimensions={
                "frequency":frequency_weights,
                "index":self.dict_attitude,
            },
            descriptor = {"Questionnair":"SOC",
                        "Factor":"Meaningfulness",
                        "Ordinal":28,
                        "Original":"How often do you have the feeling that there’s little meaning in the things you do in your daily life? "
            },
            **kwargs,
        )
        


class SOCQ29(QMLM):
    index=["index"]
    scale="frequency"
    kw_attitude_neg = ["out of control", "uncontrollable", 'unmanageable' ]
    kw_attitude_pos = ["contained", "collected", 'controlled']
    dict_attitude = dict_pos_neg(kw_attitude_pos, kw_attitude_neg, 1.0)
    def __init__(self, **kwargs):
        super().__init__(
    #         context_template="I feel that my feelings are {index}.",
    #         answer_template="It is {frequency} correct.",
            template = "I {frequency} feel that my feelings are {index}.",
            
            dimensions={
                "frequency":frequency_weights,
                "index":self.dict_attitude,
            },
            descriptor = {"Questionnair":"SOC",
                        "Factor":"Manageability",
                        "Ordinal":29,
                        "Original":"How often do you have feelings that you’re not sure you can keep under control? "
            },
            **kwargs,
        )
        
        
soc_qmlm_list = [SOCQ4, SOCQ5, SOCQ6, SOCQ8, SOCQ12, SOCQ16, SOCQ19, SOCQ21, SOCQ25, SOCQ26, SOCQ28, SOCQ29]