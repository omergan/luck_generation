from PyInquirer import style_from_dict, Token, prompt, Separator

cli_style = style_from_dict({
    Token.Separator: '#cc5454',
    Token.QuestionMark: '#673ab7 bold',
    Token.Selected: '#cc5454',  # default
    Token.Pointer: '#673ab7 bold',
    Token.Instruction: '',  # default
    Token.Answer: '#f44336 bold',
    Token.Question: '',
})

cli_instructions = [
    {
        'type': 'list',
        'message': 'Select Instruction',
        'name': 'instruction',
        'choices': [
            Separator('= Instruction menu ='),
            {
                'name': 'Generating luck: Run simulation'
            },
            {
                'name': 'Generating luck: Online data mining'
            },
            {
                'name': 'Tie Strength: Build entire graph'
            },
            {
                'name': 'Tie Strength: Build sub graph'
            },
            {
                'name': 'Tie Strength: Choose color mapping'
            },
            {
                'name': 'Tie Strength: Count parameters per layer'
            },
            {
                'name': 'Tie Strength: Extract qualification data'
            },
            {
                'name': 'Word Cloud: Generate costumer word cloud'
            },
            {
                'name': 'Word Cloud: Generate followers word cloud'
            },
            {
                'name': 'Word Cloud: Generate followers surprise words cloud'
            },
            {
                'name': 'Word Cloud: Generate 10-best followers words cloud'
            },
            {
                'name': 'Exit'
            },
        ],
        'validate': lambda answer: 'You must choose at least one instruction.' if len(answer) == 0 else True
    }
]

build_10_best_followers_word_cloud_options = [
    {
        'type': 'list',
        'message': 'Sub graph options',
        'name': 'options',
        'choices': [
            Separator('= Options menu ='),
            {
                'name': 'Surprise'
            },
            {
                'name': 'Relevance'
            },
            {
                'name': 'Back'
            },
        ],
        'validate': lambda answer: 'You must choose at least one instruction.' if len(answer) == 0 else True
    }
]

build_sub_graph_options = [
    {
        'type': 'list',
        'message': 'Sub graph options',
        'name': 'options',
        'choices': [
            Separator('= Options menu ='),
            {
                'name': 'Filter by topology'
            },
            {
                'name': 'Back'
            },
        ],
        'validate': lambda answer: 'You must choose at least one instruction.' if len(answer) == 0 else True
    }
]

choose_color_mapping_options = [
    {
        'type': 'list',
        'message': 'Color mapping options',
        'name': 'options',
        'choices': [
            Separator('= Options menu ='),
            {
                'name': 'Map by luck'
            },
            {
                'name': 'Map by relevance and surprise'
            },
            {
                'name': 'Map by relevance'
            },
            {
                'name': 'Map by surprise'
            },
            {
                'name': 'Back'
            },
        ],
        'validate': lambda answer: 'You must choose at least one instruction.' if len(answer) == 0 else True
    }
]