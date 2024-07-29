# Unate-Recursive-Complement
# Overview
- Unate Recursive Paradigm (URP) idea to determine tautology for a Boolean equation available as a SOP cube list, represented in Positional Cube Notation (PCN). It turns out that many common Boolean computations can be done using URP ideas. In this problem, we’ll first extend these ideas to do unate recursive complement. This means: we give you a file representing a Boolean function F as a PCN cube list, and you will complement it, and return F’ as a PCN cube list.
  
- The overall skeleton for URP complement is very similar to the one for URP tautology. The biggest difference is that instead of just a yes/no answer from each recursive call to the algorithm, URP complement actually returns a Boolean equation represented as a PCNcube list. We use “cubeList” as a data type in the pseudocode below. A simple version of the algorithm is below:
```bash
1. cubelist Complement( cubeList F ) {

2. // check if F is simple enough to complement it directly and quit

3. if ( F is simple and we can complement it directly )

4. return( directly computed complement of F )

5. else {

6. // do recursion

7. let x = most binate variable for splitting

8. cubeList P = Complement( positiveCofactor( F, x ) )

9. cubeList N = Complement( negativeCofactor( F, x ) )

10. P = AND( x, P )

11. N = AND( x’ , N)

12. return( OR( P, N ) )

13. } // end recursion

14. } // end function
```                      
  
