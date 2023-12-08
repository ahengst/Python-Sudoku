This is my first Python program. I tried to follow some best practices, but the code WILL show
some of my beginner habits. I'll tweak things to correct that if I have time.

Each run accepts one puzzle, then either auto-fills obvious answers or uses the process of
elimination to narrow down the remaining answers to a small number of candidates.
We do NOT do recursion yet, but that might be the only way to solve stubborn puzzles.
You may input a puzzle (symbols and spaces) as a single paste, or line by line.
Easier puzzles will be solved, but I found harder ones that it cannot solve. In that case,
make a reasonable guess and it may be able to finish it off... or not.

Current status:
Correctly solves some puzzles, with prodding by the user.

Possible improvements:
-don't print(), use logging
-allow 'solver' to be called recursively
-be more pythonic
-some places can use sets instead of lists
-this is a learning project. It may change for no good reason.
