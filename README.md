# Processamento e Recuperação de Informação 2018

Firstly install the diferent dependencies:
`numpy`
`pandas`
`sklearn`
`whoosh`
`nltk`
`spacy`

A) Run `python master.py "<argument>"` - The argument is the query to be searched. (Don't forget the `""`)

B) To see the classifier results run `python classify.py`. The results will be presented by name of classifier, followed by the precision,recall, f1-score table, and the confusion matrix.

For the prediction, change the text inside the `helpers/test1.txt`, and run `python guess.py`. The result will come in the form of `Guess: <party>`

C) Run `entities_statistics.py`.


Some files in the helpers folder are simply scripts to separate the sentences into their corresponding folders. To simplify the testing process by your part, we have not included them in the main scripts mentioned above.
