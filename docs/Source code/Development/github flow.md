This doc describes how to use git when working on the Cob project. 
## Good git practices (or 'How to git good')
Lets discuss some good git practices.

#### Strategy
The bellow strategy is based on GitHub Flow, with added details on commits.
#### Commits
Commits should have simple names. They should tell a story. As such, if we touch `main.py` to change some imports, and `utils.py` to change other imports, the worst thing to do would be:
```
$ git add --all
$ git commit -m "Changed imports" // bad
```

Instead, we should segregate commits:
```
$ git add main.py
$ git commit -m "Added numpy to main.py"
$ git add utils.py
$ git commit -m "Added sys to utils.py"
```
*(plus, with the power of squash and rebase, anyone can change the commit history to aggregate the more verbose commits. What they CANT do is separate unrelated changes)*
#### Branches
There are to be 2 levels of branch:

**1. Standard branch** - Any branch with a vague name that is long lived/permanent. `main`, etc. Pushes to these branches should not be done directly, but instead should be performed after review. Any commit on these branches should work

**2. Feature branch** - A branch created to solve a specific or very specific problem, worked on by one person but accessible to all.

Here, commits should be regular, small, and may not be operable. While preferably they should be, regular commits are better than larger commits, one commit with everything, or no commits at all. 

When reached a stable point - the code can run, mark the commit with the name "Stable: did xyz". A more verbose, multi-line name may be used. The point is to distinguish operable from WIP/unstable commits.

**Used terms:**
work - not necessarily "be fully functional", but rather "start without any hack-jobs and perform the limited set of functions implemented". If the project cant start when you click the big red shiny "start" button, that's not working. When you have to omit a broken file from the build, that's not working either. 
