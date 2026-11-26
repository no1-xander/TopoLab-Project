"""Source-grounded exercise bank for Introduction to Topology, L2 Mathematics.

Statements are transcribed from the supplied Exercise Sheets N1 and N2.
Solution notes are learning explanations, not a formal proof checker.
"""
from __future__ import annotations

EXERCISES = [
    {
        "id":"n1-e1","sheet":"N1","number":1,"title":"A finite topological space",
        "topic":"Topologies, bases, neighborhoods, operators, Hausdorff",
        "statement":"Let X={a,b,c,d} and τ={∅, X, {a}, {d}, {a,d}}.",
        "parts":[
            "Prove that τ is a topology on X.",
            "Determine all open sets and all closed sets of (X,τ).",
            "Prove that B={X,{a},{d},{a,d}} is a basis for τ.",
            "For each x∈{a,b,c}, determine its neighborhood system.",
            "For A={a,b,c}, determine int(A), cl(A), and ∂A.",
            "Is (X,τ) Hausdorff? Justify."
        ],
        "solutions":[
            "∅ and X belong to τ. The union of any subfamily is one of ∅,{a},{d},{a,d},X; intersections of two members remain in τ, hence arbitrary finite intersections do too. Thus τ is a topology.",
            "Open sets are exactly τ. Closed sets are complements in X: X,∅,{b,c,d},{a,b,c},{b,c}.",
            "Every point of every open set lies in a member of B contained in that open set; here the nonempty members of τ are themselves in B. Also B⊆τ, so B generates τ.",
            "A neighborhood is any superset of an open set containing the point. For a: all supersets of {a}; for b and c: only X, since the only open set containing either point is X.",
            "int(A)={a}; cl(A)=X because the only closed set containing A is X; ∂A=cl(A)\\int(A)={b,c,d}.",
            "No. The only open neighborhood of b and c is X, so these distinct points cannot have disjoint open neighborhoods."
        ],
        "quiz":{
            "question":"Which is the complete family of closed sets for this space?",
            "options":["{∅,X,{b,c,d},{a,b,c},{b,c}}","{∅,X,{a},{d},{a,d}}","{∅,X,{b},{c},{b,c}}","P(X)"],
            "answer":0,
            "explanation":"Closed sets are complements in X of the five open sets. The complements are X, ∅, {b,c,d}, {a,b,c}, and {b,c}."
        }
    },
    {
        "id":"n1-e2","sheet":"N1","number":2,"title":"An ordered topology on [0,1)",
        "topic":"Topologies, basis, neighborhoods, interior, closure, boundary, limit points",
        "statement":"On X=[0,1), consider τ={[0,α): 0≤α≤1}.",
        "parts":[
            "Prove that τ is a topology on X.",
            "Determine all open sets and all closed sets.",
            "Prove that B={[0,α): 0<α≤1} is a basis for τ.",
            "Describe the neighborhood system of an arbitrary x∈X.",
            "For I=[1/4,3/4], determine its interior, closure, and boundary.",
            "Determine the isolated points and accumulation points of I."
        ],
        "solutions":[
            "The empty set is obtained at α=0 and X at α=1. An arbitrary union of initial intervals is again an initial interval (or ∅); a finite intersection is the interval with the smallest endpoint. Thus τ is a topology.",
            "The open sets are exactly [0,α), 0≤α≤1. Their complements are ∅ or [α,1), for 0≤α≤1 (with [1,1)=∅).",
            "Every nonempty open set in τ is itself a member of B, so the basis criterion is immediate: each point of an open set belongs to a basis member contained in it.",
            "For x∈[0,1), the open neighborhoods are [0,α) with x<α≤1; arbitrary neighborhoods are supersets in X of at least one such interval.",
            "int(I)=∅ because every nonempty open set [0,α) contains 0 and therefore cannot be contained in I. The closure is [1/4,1): these are exactly the points whose every open neighborhood meets I. Thus ∂I=[1/4,1).",
            "No point of I is isolated: every neighborhood [0,α) of x∈I contains other points of I. The accumulation points are [1/4,1) in X."
        ],
        "quiz":{
            "question":"For x∈[0,1), which condition makes [0,α) an open neighborhood of x?",
            "options":["0≤α≤x","x<α≤1","α=x","0<α<x"],
            "answer":1,
            "explanation":"The interval [0,α) contains x exactly when x<α; α is bounded above by 1."
        }
    },
    {
        "id":"n1-e3","sheet":"N1","number":3,"title":"The usual topology on R",
        "topic":"Usual topology, neighborhoods, subbasis, separability",
        "statement":"Define τu on R as all unions of open intervals (aλ,bλ), including the empty union.",
        "parts":[
            "Prove the three topology axioms for τu.",
            "Decide whether (1,3), [1,3], [2,4), and (2,4) are neighborhoods of x=2.",
            "Show (a,b)=(a,∞)∩(-∞,b), and explain why S={(−∞,r),(r,∞):r∈R} is a subbasis.",
            "Use countability of Q and density of Q in R to prove R is separable."
        ],
        "solutions":[
            "The empty union is ∅ and R is the union of all open intervals. Arbitrary unions of unions of intervals remain such unions. The intersection of two open intervals is open or empty; distributing intersection over unions proves finite-intersection closure.",
            "(1,3) is a neighborhood of 2; [1,3] is a neighborhood because it contains (1,3); [2,4) is not, since no open interval around 2 is contained in it; (2,4) is not because it does not contain 2.",
            "A point belongs to the intersection exactly when it is greater than a and less than b. Finite intersections of subbasic rays produce open intervals, which form a basis for τu; hence S is a subbasis.",
            "Q is countable and dense. Every nonempty open interval contains a rational q, so every nonempty open set meets Q. Thus Q is a countable dense subset and R is separable."
        ],
        "quiz":{
            "question":"Which listed set is NOT a neighborhood of 2 in the usual topology?",
            "options":["(1,3)","[1,3]","[2,4)","(2,4)"],
            "answer":3,
            "explanation":"A neighborhood of 2 must contain an open interval around 2. (2,4) does not contain 2."
        }
    },
    {
        "id":"n1-e4","sheet":"N1","number":4,"title":"The induced topology",
        "topic":"Subspace topology",
        "statement":"Let X={a,b,c}, τ={∅,{a},{a,b},X}, and Y={b,c}. Find the topology induced on Y.",
        "parts":["Compute {U∩Y : U∈τ}."],
        "solutions":["Intersect each open set with Y: ∅∩Y=∅, {a}∩Y=∅, {a,b}∩Y={b}, and X∩Y=Y. Therefore τY={∅,{b},Y}."]
        ,"quiz":{"question":"What is the induced topology on Y={b,c}?","options":["{∅,{b},Y}","{∅,{c},Y}","{∅,Y}","P(Y)"],"answer":0,"explanation":"The intersections U∩Y are ∅, ∅, {b}, and Y."}
    },
    {
        "id":"n1-e5","sheet":"N1","number":5,"title":"A product topology",
        "topic":"Product topology",
        "statement":"Let X={0,1} be discrete and Y={p,q} be indiscrete. List the nonempty basic open rectangles in X×Y and determine the product topology.",
        "parts":["List the nonempty basic open rectangles.","Determine the product topology on X×Y."],
        "solutions":["The nonempty open sets in X are {0},{1},X; in Y the only nonempty open set is Y. Thus the nonempty basic rectangles are {0}×Y, {1}×Y, and X×Y.","The product topology is {∅,{(0,p),(0,q)},{(1,p),(1,q)},X×Y}."]
        ,"quiz":{"question":"How many nonempty basic open rectangles are there?","options":["2","3","4","8"],"answer":1,"explanation":"There are three nonempty open choices in X and one in Y, giving three nonempty products."}
    },
    {
        "id":"n1-e6","sheet":"N1","number":6,"title":"Hausdorff and non-Hausdorff examples",
        "topic":"Hausdorff spaces",
        "statement":"Let X={a,b}. Show that the discrete topology P(X) is Hausdorff. Is the indiscrete topology {∅,X} Hausdorff?",
        "parts":["Prove that the discrete topology is Hausdorff.","Determine whether the indiscrete topology is Hausdorff."],
        "solutions":["For the distinct points a,b, the open sets {a} and {b} are disjoint neighborhoods. This separates the only pair of distinct points.","No. The only nonempty open set is X, so any two nonempty open neighborhoods intersect in X."]
        ,"quiz":{"question":"Why is the indiscrete topology on a two-point set not Hausdorff?","options":["It has too many open sets","Distinct points have no disjoint nonempty open neighborhoods","It has no closed sets","Every singleton is open"],"answer":1,"explanation":"The only nonempty open set is X, so two nonempty open neighborhoods cannot be disjoint."}
    },
    {
        "id":"n1-e7","sheet":"N1","number":7,"title":"Interior, closure, and accumulation points",
        "topic":"Topological operators and proof",
        "statement":"Let (X,τ) be a topological space, A⊆X, and A′ the set of points whose every neighborhood meets A\\{x}. Prove the four listed properties.",
        "parts":[
            "Prove int(A) is the largest open subset of A.",
            "Prove cl(A) is the smallest closed set containing A.",
            "Prove int(X\\A)=X\\cl(A) and cl(X\\A)=X\\int(A).",
            "Prove cl(A)=A∪A′ and ∂A=cl(A)\\int(A)."
        ],
        "solutions":[
            "The interior is the union of all open subsets of A. It is open, contained in A, and contains every open subset of A, so it is the largest one.",
            "The closure is the intersection of all closed supersets of A. It is closed, contains A, and is contained in every closed superset.",
            "By the neighborhood characterization, x∉cl(A) exactly when some open neighborhood of x misses A, equivalently x∈int(X\\A). Apply this identity to X\\A to obtain the second equality.",
            "A point is in cl(A) exactly when every neighborhood meets A. This means it is in A or every neighborhood meets A\\{x}, giving A∪A′. The boundary is closure minus interior by definition."
        ],
        "quiz":{"question":"Which description characterizes cl(A) in an arbitrary topological space?","options":["The union of all open subsets of A","The intersection of all closed supersets of A","The complement of A","The set of isolated points of A"],"answer":1,"explanation":"The closure is the smallest closed set containing A, hence the intersection of all closed supersets."}
    },
    {
        "id":"n1-e8","sheet":"N1","number":8,"title":"A sequence in a discrete space",
        "topic":"Convergence",
        "statement":"Let X={a,b} have the discrete topology and define xn=a for even n and xn=b for odd n. Does (xn) converge?",
        "parts":["Determine whether the sequence converges to any point of X, using neighborhoods."],
        "solutions":["It does not converge. In a discrete space, {a} and {b} are open neighborhoods. The sequence is not eventually in {a}, nor eventually in {b}, because both values occur infinitely often."]
        ,"quiz":{"question":"What prevents the alternating sequence from converging in the discrete topology?","options":["It is unbounded","It is not eventually constant","The space is infinite","The sequence has no terms"],"answer":1,"explanation":"Convergence to a in a discrete space requires eventual membership in {a}; convergence to b requires eventual membership in {b}. Neither happens."}
    },
    {
        "id":"n1-e9","sheet":"N1","number":9,"title":"Continuity and homeomorphism",
        "topic":"Continuous maps and homeomorphisms",
        "statement":"Let X={0,1} be discrete, Y={a,b} with σ={∅,{a},Y}, and f(0)=a, f(1)=b.",
        "parts":["Find inverse images of open sets in Y and prove continuity.","Determine whether f is a homeomorphism."],
        "solutions":["f⁻¹(∅)=∅, f⁻¹({a})={0}, and f⁻¹(Y)=X. All are open in X, so f is continuous.","The inverse map g:Y→X is not continuous: the open singleton {1}⊆X has preimage g⁻¹({1})={b}⊆Y, which is not open in Y. Thus f is not a homeomorphism."]
        ,"quiz":{"question":"Is f a homeomorphism?","options":["Yes, every continuous bijection is a homeomorphism","No, the inverse map is not continuous","No, f is not injective","No, f is not continuous"],"answer":1,"explanation":"For g=f⁻¹:Y→X, the open set {1}⊆X has preimage g⁻¹({1})={b}, which is not open in Y. Hence g is not continuous."}
    },
    {
        "id":"n1-e10","sheet":"N1","number":10,"title":"The discrete metric on N",
        "topic":"Metric balls, metric topology, separability",
        "statement":"On N define d(m,n)=0 if m=n and d(m,n)=1 otherwise.",
        "parts":["Find B(3,1/2), B(3,1), and B(3,2).","Determine the generated topology and whether the metric space is separable."],
        "solutions":["For the open-ball convention d(x,3)<r: B(3,1/2)={3}, B(3,1)= {3}, and B(3,2)=N.","Every singleton is an open ball, so the generated topology is discrete. A discrete space is separable exactly when it is countable; N itself is a countable dense subset."]
        ,"quiz":{"question":"What is B(3,1) for the open-ball definition d(x,3)<1?","options":["∅","{3}","{2,3,4}","N"],"answer":1,"explanation":"Only 3 has distance strictly less than 1 from 3; all other points have distance exactly 1."}
    },
    {
        "id":"n2-e1","sheet":"N2","number":1,"title":"Compactness from the definition",
        "topic":"Compactness and open covers",
        "statement":"Answer the four compactness questions: finite discrete spaces; N discrete; R usual; and N with τ={N}∪P(N*).",
        "parts":[
            "Prove every finite discrete space is compact.",
            "Is N with the discrete topology compact?",
            "Prove R with the usual topology is not compact.",
            "For τ={N}∪P(N*), prove (N,τ) is compact."
        ],
        "solutions":[
            "Any open cover of a finite set has a finite subcover: choose one covering member for each point.",
            "No. The singleton cover {{n}:n∈N} is an open cover with no finite subcover.",
            "The cover {(-n,n): n∈N*} covers R but no finite subfamily covers R, since a finite union is bounded.",
            "Any open cover must contain N itself to cover 0, because every proper open set is a subset of N* and misses 0. Thus the one-element subcover {N} suffices."
        ],
        "quiz":{"question":"Which open cover proves that N with the discrete topology is not compact?","options":["{N}","{{n}: n∈N}","{∅,N}","{(-n,n):n∈N}"],"answer":1,"explanation":"The singleton sets form an open cover, but no finite collection covers the infinite set N."}
    },
    {
        "id":"n2-e2","sheet":"N2","number":2,"title":"Finite-intersection property and closed subspaces",
        "topic":"Compactness, FIP, closed subsets",
        "statement":"For a topological space X, prove equivalence of open-cover compactness and the finite-intersection property for closed families; then prove every closed subset of a compact space is compact.",
        "parts":["Prove the equivalence (a) every open cover has a finite subcover iff (b) every family of closed sets with FIP has nonempty total intersection.","Prove that a closed subset of a compact space is compact."],
        "solutions":["Take complements: an open cover with no finite subcover corresponds to closed complements with the finite-intersection property but empty total intersection. Conversely, a closed FIP family with empty intersection has open complements covering X; a finite subcover contradicts FIP.","Let F be closed in compact X and let {Uᵢ} cover F by sets open in the subspace. Write Uᵢ=F∩Vᵢ with Vᵢ open in X. The family {Vᵢ} together with X\\F covers X. A finite subcover of X yields finitely many Uᵢ covering F."]
        ,"quiz":{"question":"What is the key operation used to convert the open-cover condition into the FIP condition?","options":["Taking complements","Taking closures","Taking interiors","Taking Cartesian products"],"answer":0,"explanation":"Complements turn open covers into families of closed sets, and finite subcovers correspond to finite intersections."}
    },
    {
        "id":"n2-e3","sheet":"N2","number":3,"title":"Compact metric spaces",
        "topic":"Total boundedness and sequential compactness",
        "statement":"Let (X,d) be a metric space. Prove every compact metric space is totally bounded and sequentially compact.",
        "parts":["Prove every compact metric space is totally bounded.","Prove every compact metric space is sequentially compact."],
        "solutions":["For ε>0, the family {B(x,ε):x∈X} is an open cover. Compactness gives a finite subcover, whose centers form a finite ε-net.","A standard proof uses compactness to show every infinite subset has an accumulation point, then selects a subsequence with distances below 1/k from that point. If the sequence has finite range, one value repeats infinitely often and gives a constant subsequence."]
        ,"quiz":{"question":"Which family directly proves total boundedness of a compact metric space?","options":["All closed balls of radius ε","All open balls B(x,ε), for x∈X","All singleton sets","All complements of finite sets"],"answer":1,"explanation":"The open balls of fixed positive radius cover X; compactness supplies a finite subcover, which is an ε-net."}
    },
    {
        "id":"n2-e4","sheet":"N2","number":4,"title":"Finite products of compact metric spaces",
        "topic":"Product metrics, subsequences, compactness",
        "statement":"Let (X,dX) and (Y,dY) be compact metric spaces with d×((x1,y1),(x2,y2))=max{dX(x1,x2),dY(y1,y2)}.",
        "parts":["Prove every sequence in X×Y has a convergent subsequence in d×.","Deduce that (X×Y,d×) is compact."],
        "solutions":["From a sequence (xn,yn), compactness of X gives a subsequence whose first coordinates converge. From that subsequence, compactness of Y gives a further subsequence whose second coordinates converge. The first coordinates still converge along the further subsequence. The maximum of the two coordinate distances therefore tends to zero.","The product metric is a metric. The preceding argument proves sequential compactness; by the compactness criterion for metric spaces (Theorem 3.13 in Chapter 3), sequential compactness implies compactness."]
        ,"quiz":{"question":"Why does the second subsequence selection preserve convergence of the first coordinate?","options":["Every subsequence of a convergent sequence converges to the same limit","Compactness forces all points to be equal","The max metric ignores the first coordinate","The second coordinate determines the first"],"answer":0,"explanation":"A subsequence of a convergent sequence retains the same limit, so the further subsequence converges in both coordinates."}
    }
]

def get_exercises(sheet: str = "ALL") -> list[dict]:
    """Return defensive copies of exercises for the requested sheet."""
    import copy
    if sheet not in {"ALL", "N1", "N2"}:
        raise ValueError("Sheet must be ALL, N1, or N2.")
    return copy.deepcopy([e for e in EXERCISES if sheet == "ALL" or e["sheet"] == sheet])
