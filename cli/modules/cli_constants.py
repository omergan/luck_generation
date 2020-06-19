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
                'name': 'Build entire graph'
            },
            {
                'name': 'Build sub graph'
            },
            {
                'name': 'Choose color mapping'
            },
            {
                'name': 'Exit'
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
                'name': 'Filter by luck - NOT IMPLMENETED'
            },
            {
                'name': 'Filter by relevance and surprise - NOT IMPLMENETED'
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
                'name': 'Back'
            },
        ],
        'validate': lambda answer: 'You must choose at least one instruction.' if len(answer) == 0 else True
    }
]