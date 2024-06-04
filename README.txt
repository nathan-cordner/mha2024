Code for Mormon History Association 2024 presentation:

More than just quietly sitting?
An AI approach to analyzing LDS messaging about reverence and worship in General Conference

---------------

Code for the project is separated into three parts:

data_collection
---------------

Python scripts to download talks from 
-- the Journal of Discourses (https://journalofdiscourses.com/),
-- the Improvement Era (on archive.org), and 
-- other Conference Reports (from scriptures.byu.edu)

Some additional formatting is needed to get talks ready for keyword searching


sentence_analysis
-----------------

sentence_checker.py:  collect sentences from downloaded talks based on keyword
-- collected sentences are also provided in keyword folders

{sentiment,volume}_classifier.ipynb:  Python notebooks (used on Google Colab) to run HuggingFace NLP models to classify sentences
-- results of classifiers are provided in *_results folders

sentiment_then_noise.py:  visualization script to generate heatmaps and dot plots


paragraph_analysis
------------------

contains one python script to collect paragraphs from selected talks

results of running paragraphs through Microsoft Copilot are provided (as well as the chat prompts used)