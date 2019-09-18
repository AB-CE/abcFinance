# Notes

The files named Ex1-5 are those corresponding to the examples in the paper "Money creation and liquid funding needs are compatible". The other files contain related code, some of which is in development status (i.e. not tested and not guaranteed to be functional).

In order to run the code, first download the entire repository. The examples can be used as templastes. The code importing the abcFinance utilities assumes that the file is lying in a sub-subfolder of the root folder.

If you want to run through the examples one step at a time, note that the cells containing booking statements should only be executed once, because the booking statements will be recorded on each execution, which may result in assertion errors, e.g. when more cash is deducted than the agent possesses. If you wish to execute the booking statements again, then all cells starting from the declaration of the agents should be executed again, in order to reset the system and repeat the sequence of booking statements.