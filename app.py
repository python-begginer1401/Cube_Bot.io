import gradio as gr
import google.generativeai as genai
import time

# Used to securely store the API key
from google.colab import userdata
GOOGLE_API_KEY=userdata.get('gemnikey')
genai.configure(api_key=GOOGLE_API_KEY)


model = genai.GenerativeModel('gemini-1.5-flash-latest')
chat = model.start_chat(history=[])

# Transform Gradio history to Gemini format
def transform_history(history,system_prompt):
    new_history = []
    new_history.append({"parts": [{"text": system_prompt}], "role": "user"})
    for chat in history:
        new_history.append({"parts": [{"text": chat[0]}], "role": "user"})
        new_history.append({"parts": [{"text": chat[1]}], "role": "model"})
    return new_history

def response(message, history):
    global chat
    # The history will be the same as in Gradio, the 'Undo' and 'Clear' buttons will work correctly.
    system_prompt = f"""
    you are a cubing algorithm fetcher you will give the user the cubing algorithm to the case they give you and respond in no more than 150 words make sure that the algorithm you give them is written with cubing notations for example OLL 50
    r' U r2 U' r2 U' r2 U r' also make sure the algorithms are correct also this is only for 3 by 3 cubes Here Are all of the oll cases so you don't get confused : No Edges Solved
Picture
OLL 1
R U2 (R2 F R F’) U2 (R’ F R F’)
Similar to 35
Picture
OLL 2
​l’ U’ l (U2 L’ U2 L U2) R’ F R
Picture
OLL 3
F (U R U’ R’) F' U F (R U R’ U’) F’
Mirror of 4
Picture
OLL 4
F’ (U’ L’ U L) F U F (R U R’ U’) F’
​Mirrored set up move then same as 3
Picture
OLL 18
(F R’ F’ R) (U R U’ R’) U F (R U R’ U’) F’
Almost same as 19
Picture
OLL 19
(F R’ F’ R) (U R U’ R’) U' F (R U R’ U’) F’
​Almost same as 18
Picture
OLL 17
(R U R’ U) (R’ F R F’) U2 (R’ F R F’)





Picture
OLL 20
(M’ U2 M U2) M’ U M (U2 M' U2 M)
L-Shaped Edges Solved
No Corners Solved
Picture
OLL 48
F (R U R’ U’)2x F’
Mirror of 47 Similar to 45

Picture
OLL 47
F’ (L' U' L U)2x F
Mirror of 48
Picture
OLL 53
r’ U’ r (R' U’ R U)2x r’ U r
​Mirror of 54 Reverse of 56
Picture
OLL 54
l U l’ (L U L’ U’)2x l U’ l’
​Mirror of 53
Picture
OLL 49
​l U' l2 U l2 U l2 U' l
​or
R B’ R2 F R2 B R2 F’ R
​Mirror of 50


Picture
OLL 50
r' U r2 U' r2 U' r2 U r'
​or
L’ B L2 F’ L2 B’ L2 F L’
​Mirror of 49
1 Corner Solved
Picture
OLL 5
l’ U2 (L U L’ U) l
Mirror of 6
Picture
OLL 6
r U2 (R’ U’ R U’) r’
Mirror of 5
Picture
OLL 7
l (U L’ U L) U2 l’
​Backwards 5
Picture
OLL 8
r’ (U’ R U’ R’) U2 r ​
​Backwards 6
Picture
OLL 11
M (R U R’ U) (R U2 R’ U) M’
Mirror of 12
Picture
OLL 12
M (L’ U’ L U’) (L’ U2 L U’) M’
​Mirror of 11
Picture
OLL 9
(R U R’ U') R' F R (R U R’ U') F'
​or
R’ U’ R y (r U’ r’ U) r U r’
​Mirror of 10 Reverse of 13
Picture
OLL 10
(L' U' L U) L F' L' (L' U' L U) F
or
L U L' y' (l' U l U') l' U' l
Mirror of 9 Reverse of 14
2 Corners Solved
Picture
OLL 44
​F (U R U’ R’) F’
Picture
OLL 43
​F’ (U’ L’ U L) F
Mirror of 44
Picture
OLL 31
R’ U’ F (U R U’ R’) F’ R
​Mirror of 32 Reverse of 40
Picture
OLL 32
​L U F’ (U’ L’ U L) F L’
Mirror of 31 Reverse of 39
Picture
OLL 35
R U2 (R2 F R F’) R U2 R’
​Similar to 1
Picture
OLL 37
F R U' R' U' R U R' F'
​or
(F R’ F’ R) (U R U’ R’)
​Reverse of 33
Picture
OLL 36
(R’ U’ R U’) (R’ U R U) (R B’ R’ B)
​Mirror of 38
Picture
OLL 38
(L U L’ U) (L U’ L’ U’) (L’ B L B’)
Mirror of 36
Picture
OLL 29
M U (R U R’ U’) (R’ F R F’) M’
Mirror of 30
Picture
OLL 30
M U’ (L’ U’ L U) (L F’ L' F) M'
​Mirror of 29
Picture
OLL 41
M U F (R U R’ U’) F' M’
or
L’ U L U2 L’ U’ y’ (L' U L U) F ​
Mirror of 42
Picture
OLL 42
M U' F' (L' U' L U) F M’
​or
R U’ R’ U2 R U y (R U’ R’ U’) F’ ​
Mirror of 41
4 Corners Solved
Picture
OLL 28
M’ U M U2 M’ U M

Bar-Shaped Edges Solved
No Corners Solved
Picture
OLL 51
F (U R U’ R’)2X F’
​Reverse of 48
Picture
OLL 56
r' U' r (U' R' U R)2x r' U r
Reverse of 53
Picture
OLL 52
(R U R’ U) R d’ R U’ R’ F'



Picture
OLL 55
​R U2 R2 (U’ R U’ R’) U2 (F R F')
1 Corner Solved
Picture
OLL 15
r’ U’ r (R’ U’ R U) r’ U r
Mirror of 16
Picture
OLL 16
l U l’ (L U L’ U’) l U’ l’
Mirror of 15
Picture
OLL 13
r U’ r’ (U’ r U r’) y’ R’ U R
​Reverse of 14 Mirror of 9
Picture
OLL 14
l’ U l (U l’ U’ l) y L U’ L’
​Reverse of 13 Mirror of 10
2 Corners Solved
Picture
OLL 33
(R U R’ U’) (R’ F R F’)
Reverse of 37
Picture
OLL 45
F (R U R’ U’) F’
Reverse of 44
Picture
OLL 34
(R U R’ U’) B’ (R’ F R F’) B
Picture
OLL 46
R’ U’ (R’ F R F’) U R




Picture
OLL 40
R’ F (R U R’ U’) F’ U R
​Mirror of 39 reverse of 31
Picture
OLL 39
L F’ (L’ U’ L U) F U’ L’
​Mirror of 40 reverse of 32
4 Corners Solved
Picture
OLL 57
​(R U R’ U’) r (R’ U R U’) r’
or
M' U M' U M' d2 M' U M' U M'

4 Edges Solved
​(All Algorithms for Corners portion of 2-Look OLL)
Picture
OLL 21
F (R U R’ U’)3x F’
Similar to 45
Picture
OLL 22
R U2 (R2 U' R2 U' R2) U2 R




Picture
OLL 27 Sune
R U R' U R U2 R'




Picture
OLL 26
L' U' L U' L' U2 L
Picture
OLL 25
(R' F R B') (R' F' R B)




Picture
OLL 23
(R2 D R' U2) (R D' R' U2) R'
Picture
OLL 24
​(r U R' U') (r' F R F')


Here are all of the PLL cases : Mirrored Algorithms
Picture
PLL Aa
(R' F R' B2) (R F' R' B2) R2
Mirror of Ab
Used for 2-look corners
Picture
PLL Ab
(L F' L B2) (L' F L B2) L2
Mirror of Aa

Picture
PLL Ua
(R U' (R U R U) R U') R' U' R2
Mirror of Ub
Used in 2-Look Edges
​
Picture
PLL Ub
(L' U (L' U' L' U') L' U) L U L2
Mirror of Ua
​Used in 2-Look Edges

Picture
PLL Nb
​(R' U L' U2 R U' L)2x
or
L' U' L U'
L' U' L F (L' U' L U) L F' L2 U L U2 L' U L
Mirror of Na
​​Used in 2-Look Corners
Picture
PLL Na
​(L U' R U2 L' U R')2x
or
​R U R' U
R U R' F' (R U R' U') R' F R2 U' R' U2 R U' R'
Mirror of Nb


Picture
PLL Jb
R U R' F' (R U R' U') R' F R2 U' R' U'
Mirror of Ja
​
Picture
PLL Ja
L' U' L F (L' U' L U) L F' L2 U L U
Mirror of Jb

Picture
PLL Rb
R' U2 R U2 R' F (R U R' U') R' F' R2 U'
Mirror of Ra
​
Picture
PLL Ra
L U2 L' U2 L F' (L' U' L U) L F L2 U
Mirror of Rb

G Permutations
(Mirrored and Reverse of 1 algorithm)
Picture
PLL Gd
R U R' y' R2 u' (R U' R' U R') u R2

Picture
PLL Gb
L' U' L y L2 u (L' U  L U' L) u' L2
Mirror of Gd
Picture
PLL Ga
R2 u (R’ U R’ U’ R) u' R2 y’ R’ U R
​Reverse of Gd
Picture
​Gc
L2 u' (L U' L U L') u L2 y L U' L'
Reverse of Gb/Mirror of Ga
Other Algorithms
Picture
PLL H
M2 U M2 U2 M2 U M2​
​Used in 2-Look Edges
Picture
PLL Z
(M2 U M2 U) M' (U2 M2 U2) M' U2
​Used in 2-Look Edges

Picture
PLL T
(R U R' U') R' F R2 U' R' U' R U R' F'
Similar to F
Picture
PLL F
R' U' F'
(R U R' U') R' F R2 U' R' U' R U R' U R
Similar to﻿ T with set up move

Picture
PLL Y
F (R U' R' U') R U R' F' (R U R' U') R' F R F'
Picture
PLL V
R' U R' d' R' F' R2 U' R' U R' F R F

Picture
PLL E
(R B' R' F)(R B R' F')(R B R' F)(R B' R' F')
or
R2 U R' U' y (R U R' U')2x R U R' y' R U' R2 also add emojis when responding
    """
    chat.history = transform_history(history,system_prompt)
    response = chat.send_message(message)
    response.resolve()

    # Each character of the answer is displayed
    for i in range(len(response.text)):
        time.sleep(0.005)
        yield response.text[: i+20]

iface = gr.ChatInterface(response,
                 title='Cube_Bot.io',
                 textbox=gr.Textbox(placeholder="What case do you need help solving? (for example OLL 50)"),
                 retry_btn=None).launch(debug=True)

iface.launch()
