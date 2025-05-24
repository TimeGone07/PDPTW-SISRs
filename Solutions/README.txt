
## Structure of solution files.

"Instances for the Pickup and Delivery Problem with Time Windows 
 based on open data"

===============================================================================
===============================================================================

Solution files follow the same structure from the SINTEF TOP website

https://www.sintef.no/projectweb/top/pdptw/

The file contains a header with four information fields:

Instance name:    <name of the instance>
Authors:          <name of the authors who found the solution>
Date:             <date when solution was found yyyy-mm-dd>
Reference:        <a reference to the work with title or report number>

This is followed by a line with the word "Solution", and then
as many lines as there are routes in this solution, detailing every
vehicle route. This is done by using the structure

		Route X : n1 n2 n3 n4 ... nk

Where X is the index of the route and n1,n2,n3,n4,nk are the nodes
of this route, which contain k locations.

NOTE: the depot is not included in the reporting of the routes.


We also follow the naming convention of SINTEF for solution files.
That is, a solution with V vehicles and cost C for the instance file 
"inst.txt" will have the name

	 inst.V_C.txt

===============================================================================
===============================================================================

EXAMPLE:
    As an example, consider the following solution with 6 routes.


Instance name:    bar-n100-1
Authors:          Carlo Sartori and Luciana Buriol
Date:             2019-2-11
Reference:        A matheuristic approach to the PDPTW (to be submitted).
Solution
Route 1 : 31 44 35 81 16 66 32 82 19 85 94 69
Route 2 : 29 21 71 27 47 79 11 22 97 77 72 6 61 25 56 75 1 51
Route 3 : 40 48 9 59 5 55 90 98 41 8 10 91 60 38 28 78 88 58
Route 4 : 26 76 30 80 7 39 57 42 92 12 89 18 62 68 37 36 87 50 100 86
Route 5 : 14 15 64 49 45 43 65 4 99 46 95 96 54 93 23 73
Route 6 : 33 13 63 20 83 17 67 2 34 52 84 24 70 74 3 53



This solution file is named:

	 bar-n100-1.6_733.txt

===============================================================================
===============================================================================

## Carlo Sartori and Luciana Buriol (2019).



