<!-- This is a comment block in Markdown. When the document is rendered, you won't see this text.

If you need help on MarkDown syntax, you can look at the guide here: https://www.markdownguide.org/basic-syntax/.
You are also welcome to ask the Module instructors for help with writing MarkDown.

You can use this template as the starting point for your report.
Answer the questions by writing your answers in the space between the bullet points.
If you are editing this file in VSCode, you can press CTRL+K then V to open a preview of the document.

Comment blocks end by closing the "arrow" we opened at the start. -->

# Determining Depot Locations: Report

<!-- This module is anonymously marked - please DO NOT include your name! -->
Candidate Number:

<!-- The headers that follow correspond to all questions in the assignment that require a written answer. 

You can write as much as you like for your answers in the space provided.
However please bear in mind that a good answer and a long answer are not necessarily the same thing! -->

## `Location` equality

1. Why might the definition of "equal" not be desirable, if we did not have the assurance from CLtd at the start of this task?

<YOUR ANSWER HERE>

2. Are there any problems you foresee with this definition of "equal", even with the assurance (at the start of this task) from CLtd?

<YOUR ANSWER HERE>

3. Suggest an idea for avoiding / resolving the problem you raised in point 2, if you identified any. Choose one of your choice if you identified multiple issues. **Do not** implement this idea in your code, however.

<YOUR ANSWER HERE>

## Fastest Trip From a Given `Location`

1. Is it possible, even after the tie-breakers given in the assignment task, for there to still be multiple entries in `potential_locations` to choose as the closest? (Yes/ No)

Yes / No

2. If not, why not? If so, what are the circumstances under which this could happen?

<YOUR ANSWER HERE>

3. How can you edit the method to fix the problem (if there is one) without forcing an error to be thrown? (Do not forget, you should implement these fixes in your code if you identify any here).

<YOUR ANSWER HERE>

## Execution Time for the NNA

1. Identify (at least) one aspect of the `regular_n_gon` that makes it difficult to understand, or that might make it difficult to understand in the future. Suggest how this might be addressed.

<YOUR ANSWER HERE>

2. Assess the advantages and disadvantages of using `Country`s like those generated from `regular_n_gon` for gathering the execution times $t_{\text{exe}}$, as opposed to a `Country` like the one in `locations.csv` or a `Country` with randomly-distributed settlements. You should give at least one advantage or one disadvantage.

<YOUR ANSWER HERE>

3. Comment on the relationship between the execution time $t_{\text{exe}}$ and number of settlements $N_{\text{locs}}$, given the data in your plot. You should include your plot as an image here.

<YOUR ANSWER HERE>

![This line will include your plot as an image in your report. This text will be displayed if your plot file cannot be found.](./nna_execution_times.png)

4. Why do you think $t_{\text{exe}}$ and $N_{\text{locs}}$ have this kind of relationship?

<YOUR ANSWER HERE>
