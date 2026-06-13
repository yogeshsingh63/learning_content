# Ultimate DSA Revision Handbook for Coding Interviews

1

# DSA Roadmap Overview

This handbook is designed for someone who has **completed DSA once** (primarily in C++) and needs a structured, comprehensive revision before coding interviews. Each topic below builds upon the previous one. Follow this roadmap sequentially for maximum retention, or jump to any section for targeted revision.

**How to use this handbook:** Each section contains theory, intuition, C++ implementations, dry runs, complexity analysis, common mistakes, interview questions, and pattern recognition guides. Use the checkboxes to track your progress — your state is saved automatically in your browser.

### The Complete Roadmap

Phase 1: Foundations ├── 1. Complexity Analysis (Big O, Amortized) ├── 2. Arrays (Prefix Sum, Kadane, DNF) ├── 3. Strings (KMP, Rabin-Karp, Z-Algo) └── 4. Hashing (Frequency, Lookup) Phase 2: Linear Data Structures ├── 5. Linked Lists (Fast-Slow, In-place Reversal) ├── 6. Stack (Monotonic Stack Patterns) └── 7. Queue / Deque (Sliding Window Max) Phase 3: Recursion & Search ├── 8. Recursion (Call Stack, Subsequences) ├── 9. Backtracking (N-Queens, Sudoku) ├── 10. Binary Search (Search/Answer Space) ├── 11. Two Pointers (Pair Sum, 3Sum) └── 12. Sliding Window (Fixed/Variable) Phase 4: Sorting & Trees ├── 13. Sorting (Merge, Quick, Heap Sort) ├── 14. Trees (Traversals, DFS, BFS) ├── 15. BST (Validate, LCA, Kth Smallest) ├── 16. Heap / Priority Queue (Top-K) └── 17. Trie (Prefix Matching) Phase 5: Graphs ├── 18. Graph Basics (BFS, DFS, Cycle Detection) └── 19. Advanced (Dijkstra, MST, Topo Sort, DSU) Phase 6: Paradigms ├── 20. Greedy (Activity Selection, Intervals) └── 21. Dynamic Programming (All Patterns) Phase 7: Advanced ├── 22. Bit Manipulation (XOR Tricks) ├── 23. Segment Tree (Range Queries) ├── 24. Fenwick Tree / BIT └── 25. Disjoint Set Union

### Estimated Timeline

Phase

Topics

Suggested Days

Phase 1

Foundations

4–5 days

Phase 2

Linear Structures

3–4 days

Phase 3

Recursion & Search

5–6 days

Phase 4

Sorting & Trees

5–6 days

Phase 5

Graphs

4–5 days

Phase 6

Paradigms

7–10 days

Phase 7

Advanced

3–4 days

2

# Complexity Analysis

### Asymptotic Notations

#### Big O — O(f(n)) — Upper Bound

**Definition:** f(n) = O(g(n)) if there exist constants c > 0 and n₀ ≥ 0 such that f(n) ≤ c·g(n) for all n ≥ n₀. It describes the **worst-case** growth rate of an algorithm.

**Intuition:** "My algorithm will _never_ be slower than this." It's the ceiling on performance. When someone says "this algorithm is O(n log n)", they mean: in the worst scenario, it grows at most proportional to n·log(n).

#### Big Omega — Ω(f(n)) — Lower Bound

**Definition:** f(n) = Ω(g(n)) if there exist constants c > 0 and n₀ such that f(n) ≥ c·g(n) for all n ≥ n₀. It describes the **best-case** growth rate.

**Intuition:** "My algorithm will _always_ take at least this much time." Comparison-based sorting, for example, has Ω(n log n) — you can't do better.

#### Big Theta — Θ(f(n)) — Tight Bound

**Definition:** f(n) = Θ(g(n)) if f(n) = O(g(n)) AND f(n) = Ω(g(n)). The function grows at _exactly_ that rate asymptotically.

**Intuition:** "My algorithm is _precisely_ this fast." Merge sort is Θ(n log n) — it's always n log n regardless of input order.

#### Amortized Analysis

**Definition:** Average time per operation over a worst-case sequence of operations. Not the same as average-case analysis.

**Classic Example — Dynamic Array (std::vector):** Appending is usually O(1), but occasionally O(n) when the array doubles. Over n insertions, total cost is O(n), making the amortized cost per insertion O(1).

**Interview Tip:** When asked "Is push\_back O(1) or O(n)?", the correct answer is "O(1) amortized." Explain the doubling strategy.

### Common Complexities — Reference Table

Complexity

Name

n=10⁶ Operations

Example Algorithms

O(1)

Constant

1

Array access, hash lookup

O(log n)

Logarithmic

~20

Binary search, balanced BST ops

O(√n)

Square Root

~1000

Trial division, sqrt decomposition

O(n)

Linear

10⁶

Linear search, single pass

O(n log n)

Linearithmic

~2×10⁷

Merge sort, heap sort

O(n²)

Quadratic

10¹²

Bubble sort, nested loops

O(2ⁿ)

Exponential

Impossible

Subsets, brute-force TSP

O(n!)

Factorial

Impossible

Permutations, brute-force

### How to Analyze Complexity

*   **Single loop** iterating n times → O(n)
*   **Nested loops**, both iterating n → O(n²)
*   **Loop dividing n by 2 each time** → O(log n)
*   **Loop inside a halving loop** → O(n log n)
*   **Two separate sequential loops** → O(n) + O(n) = O(n)
*   **Recursive call** with two branches of size n/2 and O(n) merge → O(n log n) (Master theorem)

### Master Theorem Quick Reference

For recurrences of the form T(n) = a·T(n/b) + O(nᵈ):

Condition

Result

d > log\_b(a)

T(n) = O(nᵈ)

d = log\_b(a)

T(n) = O(nᵈ · log n)

d < log\_b(a)

T(n) = O(n^(log\_b(a)))

### Space Complexity Rules

*   **Iterative** with constant extra vars → O(1) space
*   **Recursive** call stack depth d → O(d) space
*   **Creating a copy** of input → O(n) space
*   **Matrix / 2D DP** → O(n×m) space

▶ Interview Questions — Complexity Analysis

*    What is the time complexity of binary search? Why?
*    Explain amortized analysis of vector::push\_back.
*    What is the difference between O, Ω, and Θ?
*    What is the time complexity of finding all subsets of a set?
*    Use the Master Theorem to solve T(n) = 2T(n/2) + n.
*    Why is hash table lookup O(1) amortized but O(n) worst-case?
*    What is the space complexity of merge sort vs quick sort?

3

# Arrays

Arrays are the most fundamental data structure. Mastering array manipulation patterns is critical because nearly every interview starts with an array problem. The key insight is that array problems are pattern-matching exercises — once you recognize the pattern, the solution becomes mechanical.

### Pattern 1: Prefix Sum

#### Intuition

Precompute cumulative sums so that any subarray sum can be answered in O(1). If prefix\[i\] stores sum of elements from index 0 to i, then sum(l..r) = prefix\[r\] - prefix\[l-1\].

#### When to Use

Any problem asking for _subarray sums_, _range queries_, or _cumulative frequency_.

C++Copy

```cpp
// Prefix Sum Template
vector<int> buildPrefix(const vector<int>& arr) {
    int n = arr.size();
    vector<int> prefix(n + 1, 0);
    for (int i = 0; i < n; i++)
        prefix[i + 1] = prefix[i] + arr[i];
    return prefix;
}

// Query: sum of arr[l..r] (0-indexed)
int rangeSum(const vector<int>& prefix, int l, int r) {
    return prefix[r + 1] - prefix[l];
}
```

Time: O(n) build, O(1) per query. Space: O(n)

### Pattern 2: Kadane's Algorithm — Maximum Subarray Sum

#### Intuition

At every index, decide: extend the current subarray, or start a new one. If the running sum drops below 0, starting fresh is always better. This is essentially a _local vs global_ maximum decision at each step.

C++Copy

```cpp
// Kadane's Algorithm — Maximum Subarray Sum
int maxSubarraySum(const vector<int>& nums) {
    int maxSum = nums[0], curSum = nums[0];
    for (int i = 1; i < nums.size(); i++) {
        curSum = max(nums[i], curSum + nums[i]);
        maxSum = max(maxSum, curSum);
    }
    return maxSum;
}

// Variant: Return the subarray itself
pair<int, pair<int,int>> maxSubarrayWithIndices(const vector<int>& nums) {
    int maxSum = nums[0], curSum = nums[0];
    int start = 0, end = 0, tempStart = 0;
    for (int i = 1; i < nums.size(); i++) {
        if (nums[i] > curSum + nums[i]) {
            curSum = nums[i];
            tempStart = i;
        } else {
            curSum += nums[i];
        }
        if (curSum > maxSum) {
            maxSum = curSum;
            start = tempStart;
            end = i;
        }
    }
    return {maxSum, {start, end}};
}
```

Time: O(n) Space: O(1)

Dry Run: arr = \[-2, 1, -3, 4, -1, 2, 1, -5, 4\] i=0: curSum = -2, maxSum = -2 i=1: curSum = max(1, -2+1) = 1, maxSum = 1 i=2: curSum = max(-3, 1-3) = \-2, maxSum = 1 i=3: curSum = max(4, -2+4) = 4, maxSum = 4 i=4: curSum = max(-1, 4-1) = 3, maxSum = 4 i=5: curSum = max(2, 3+2) = 5, maxSum = 5 i=6: curSum = max(1, 5+1) = 6, maxSum = 6 ← answer i=7: curSum = max(-5, 6-5) = 1, maxSum = 6 i=8: curSum = max(4, 1+4) = 5, maxSum = 6 Answer: 6 (subarray \[4,-1,2,1\])

### Pattern 3: Dutch National Flag (3-way Partition)

#### Intuition

Partition an array of 0s, 1s, and 2s in-place using three pointers: _low_ (boundary of 0s), _mid_ (current element), _high_ (boundary of 2s). Process elements from left to right, swapping into the correct region.

C++Copy

```cpp
// Dutch National Flag — Sort 0s, 1s, 2s
void sortColors(vector<int>& nums) {
    int low = 0, mid = 0, high = nums.size() - 1;
    while (mid <= high) {
        if (nums[mid] == 0) {
            swap(nums[low], nums[mid]);
            low++; mid++;
        } else if (nums[mid] == 1) {
            mid++;
        } else { // nums[mid] == 2
            swap(nums[mid], nums[high]);
            high--;
            // Don't increment mid — swapped element needs inspection
        }
    }
}
```

Time: O(n) single pass. Space: O(1)

**Common Mistake:** Incrementing `mid` after swapping with `high`. The swapped element hasn't been inspected yet — you must check it in the next iteration.

### Pattern 4: Merge Intervals

C++Copy

```cpp
// Merge Overlapping Intervals
vector<vector<int>> merge(vector<vector<int>>& intervals) {
    sort(intervals.begin(), intervals.end());
    vector<vector<int>> merged;
    for (auto& interval : intervals) {
        if (merged.empty() || merged.back()[1] < interval[0]) {
            merged.push_back(interval);
        } else {
            merged.back()[1] = max(merged.back()[1], interval[1]);
        }
    }
    return merged;
}
```

Time: O(n log n) due to sorting. Space: O(n)

### Pattern 5: Difference Array

#### Intuition

When you need to apply many range-increment operations (add val to all elements from l to r), instead of updating each element, mark the start and end of each range in a difference array. Then reconstruct with a prefix sum.

C++Copy

```cpp
// Difference Array — Efficient Range Updates
// Apply q range updates, each adding val to arr[l..r]
vector<int> applyRangeUpdates(int n, vector<tuple<int,int,int>>& updates) {
    vector<int> diff(n + 1, 0);
    for (auto& [l, r, val] : updates) {
        diff[l] += val;
        diff[r + 1] -= val;
    }
    // Reconstruct with prefix sum
    vector<int> result(n);
    result[0] = diff[0];
    for (int i = 1; i < n; i++)
        result[i] = result[i-1] + diff[i];
    return result;
}
```

Time: O(n + q) for q updates on array of size n. Space: O(n)

### Key Problems — Implementations

▶ Two Sum — Hash Map Approach

C++Copy

```cpp
// Two Sum — O(n) using hash map
vector<int> twoSum(vector<int>& nums, int target) {
    unordered_map<int, int> seen; // value -> index
    for (int i = 0; i < nums.size(); i++) {
        int complement = target - nums[i];
        if (seen.count(complement))
            return {seen[complement], i};
        seen[nums[i]] = i;
    }
    return {}; // no solution
}
```

Time: O(n) Space: O(n)

▶ Product of Array Except Self

##### Intuition

For each index i, the answer is (product of all elements left of i) × (product of all elements right of i). Build left-products in a forward pass, then multiply with right-products in a backward pass, reusing the output array.

C++Copy

```cpp
// Product of Array Except Self — No division, O(1) extra space
vector<int> productExceptSelf(vector<int>& nums) {
    int n = nums.size();
    vector<int> ans(n, 1);

    // Forward pass: ans[i] = product of nums[0..i-1]
    int leftProduct = 1;
    for (int i = 0; i < n; i++) {
        ans[i] = leftProduct;
        leftProduct *= nums[i];
    }

    // Backward pass: multiply by product of nums[i+1..n-1]
    int rightProduct = 1;
    for (int i = n - 1; i >= 0; i--) {
        ans[i] *= rightProduct;
        rightProduct *= nums[i];
    }
    return ans;
}
```

Time: O(n) Space: O(1) (output array doesn't count)

▶ Best Time to Buy and Sell Stock

C++Copy

```cpp
// Best Time to Buy and Sell Stock — Single Transaction
int maxProfit(vector<int>& prices) {
    int minPrice = INT_MAX, maxProfit = 0;
    for (int price : prices) {
        minPrice = min(minPrice, price);
        maxProfit = max(maxProfit, price - minPrice);
    }
    return maxProfit;
}
```

Time: O(n) Space: O(1)

▶ Majority Element — Boyer-Moore Voting

##### Intuition

If an element appears more than n/2 times, pair each occurrence with a different element. After cancellation, the majority element survives. Use a candidate and counter: increment if same, decrement if different. When counter hits 0, switch candidate.

C++Copy

```cpp
// Boyer-Moore Voting Algorithm
int majorityElement(vector<int>& nums) {
    int candidate = 0, count = 0;
    for (int num : nums) {
        if (count == 0) candidate = num;
        count += (num == candidate) ? 1 : -1;
    }
    return candidate; // guaranteed to exist
}
```

Time: O(n) Space: O(1)

▶ Rotate Array

##### Intuition

Rotating right by k is equivalent to: reverse the whole array, reverse the first k, reverse the rest. Three reverses, O(1) space.

C++Copy

```cpp
// Rotate Array — Right rotation by k steps
void rotate(vector<int>& nums, int k) {
    int n = nums.size();
    k %= n;
    reverse(nums.begin(), nums.end());
    reverse(nums.begin(), nums.begin() + k);
    reverse(nums.begin() + k, nums.end());
}
```

Time: O(n) Space: O(1)

▶ Common Mistakes & Interview Tips — Arrays

**Common Mistakes:**

*   Off-by-one errors in prefix sum queries (0-indexed vs 1-indexed).
*   Not handling empty arrays or single-element arrays.
*   Forgetting to take k % n in rotation problems.
*   Using int when products can overflow — use long long.
*   Modifying array while iterating with index-based logic.

**Interview Tips:**

*   Always clarify: Is the array sorted? Are there duplicates? Can it be negative?
*   Start by brute force, then optimize. Don't jump to the optimal solution.
*   If asked "can you do it in O(1) space?", think: two pointers, swap-based, or reversal trick.

4

# Strings

String problems test your understanding of character manipulation, hashing, and pattern matching. In C++, `std::string` is mutable (unlike Java/Python), which gives you advantages for in-place operations.

### KMP Algorithm — Knuth-Morris-Pratt

#### Intuition

Naive pattern matching is O(n×m) because after a mismatch, you restart from the next character. KMP avoids this by precomputing a **Longest Proper Prefix which is also Suffix (LPS)** array for the pattern. When a mismatch occurs at pattern\[j\], instead of restarting, jump to LPS\[j-1\] — because that prefix has already been matched.

#### LPS Array Construction

LPS\[i\] = length of the longest proper prefix of pattern\[0..i\] which is also a suffix. This tells us "how much of the pattern we've already matched" after a mismatch.

C++Copy

```cpp
// KMP Pattern Matching Algorithm
vector<int> buildLPS(const string& pattern) {
    int m = pattern.size();
    vector<int> lps(m, 0);
    int len = 0, i = 1;
    while (i < m) {
        if (pattern[i] == pattern[len]) {
            len++;
            lps[i] = len;
            i++;
        } else {
            if (len != 0)
                len = lps[len - 1]; // Don't increment i
            else {
                lps[i] = 0;
                i++;
            }
        }
    }
    return lps;
}

vector<int> kmpSearch(const string& text, const string& pattern) {
    int n = text.size(), m = pattern.size();
    vector<int> lps = buildLPS(pattern);
    vector<int> matches;
    int i = 0, j = 0;
    while (i < n) {
        if (text[i] == pattern[j]) {
            i++; j++;
        }
        if (j == m) {
            matches.push_back(i - j); // Match found at index i-j
            j = lps[j - 1];
        } else if (i < n && text[i] != pattern[j]) {
            if (j != 0)
                j = lps[j - 1];
            else
                i++;
        }
    }
    return matches;
}
```

Time: O(n + m) Space: O(m)

Dry Run — LPS for "AAACAAAA": pattern: A A A C A A A A index: 0 1 2 3 4 5 6 7 LPS\[0\] = 0 (by definition) LPS\[1\] = 1 (A == A, prefix "A" = suffix "A") LPS\[2\] = 2 (AA == AA) LPS\[3\] = 0 (no prefix = suffix ending in C) LPS\[4\] = 1 (A == A) LPS\[5\] = 2 (AA == AA) LPS\[6\] = 3 (AAA == AAA) LPS\[7\] = 3 (AAC ≠ AAA, fallback → 3) LPS = \[0, 1, 2, 0, 1, 2, 3, 3\]

### Rabin-Karp Algorithm — Rolling Hash

#### Intuition

Instead of comparing characters one by one, compute a hash of the pattern and compare it with hash of every window of the same size in the text. If hashes match, verify character by character (to handle collisions). Use a **rolling hash** to update the window hash in O(1).

C++Copy

```cpp
// Rabin-Karp with Rolling Hash
vector<int> rabinKarp(const string& text, const string& pattern) {
    int n = text.size(), m = pattern.size();
    if (m > n) return {};
    const long long MOD = 1e9 + 7, BASE = 31;
    vector<int> matches;

    // Compute hash of pattern and first window
    long long patHash = 0, winHash = 0, power = 1;
    for (int i = 0; i < m; i++) {
        patHash = (patHash + (pattern[i] - 'a' + 1) * power) % MOD;
        winHash = (winHash + (text[i] - 'a' + 1) * power) % MOD;
        if (i < m - 1) power = (power * BASE) % MOD;
    }

    for (int i = 0; i <= n - m; i++) {
        if (patHash == winHash) {
            // Verify character by character
            if (text.substr(i, m) == pattern)
                matches.push_back(i);
        }
        // Slide window: remove text[i], add text[i+m]
        if (i < n - m) {
            winHash = (winHash - (text[i] - 'a' + 1) + MOD) % MOD;
            winHash = (winHash / BASE) % MOD; // Note: use modular inverse in practice
            winHash = (winHash + (text[i + m] - 'a' + 1) * power) % MOD;
        }
    }
    return matches;
}
```

Time: O(n + m) average, O(n × m) worst (hash collisions). Space: O(1)

### Z Algorithm

#### Intuition

Z\[i\] = length of the longest substring starting at i which is also a prefix of the string. For pattern matching, concatenate pattern + "$" + text and compute Z-array. Any Z\[i\] == m indicates a match.

C++Copy

```cpp
// Z Algorithm
vector<int> zFunction(const string& s) {
    int n = s.size();
    vector<int> z(n, 0);
    int l = 0, r = 0;
    for (int i = 1; i < n; i++) {
        if (i < r)
            z[i] = min(r - i, z[i - l]);
        while (i + z[i] < n && s[z[i]] == s[i + z[i]])
            z[i]++;
        if (i + z[i] > r) {
            l = i;
            r = i + z[i];
        }
    }
    return z;
}

// Pattern matching using Z Algorithm
vector<int> zSearch(const string& text, const string& pattern) {
    string concat = pattern + "$" + text;
    vector<int> z = zFunction(concat);
    vector<int> matches;
    int m = pattern.size();
    for (int i = m + 1; i < concat.size(); i++)
        if (z[i] == m)
            matches.push_back(i - m - 1);
    return matches;
}
```

Time: O(n + m) Space: O(n + m)

▶ More String Problems

C++Copy

```cpp
// Longest Common Prefix
string longestCommonPrefix(vector<string>& strs) {
    if (strs.empty()) return "";
    string prefix = strs[0];
    for (int i = 1; i < strs.size(); i++) {
        while (strs[i].find(prefix) != 0) {
            prefix = prefix.substr(0, prefix.size() - 1);
            if (prefix.empty()) return "";
        }
    }
    return prefix;
}

// Valid Anagram
bool isAnagram(string s, string t) {
    if (s.size() != t.size()) return false;
    int freq[26] = {};
    for (char c : s) freq[c - 'a']++;
    for (char c : t) freq[c - 'a']--;
    for (int f : freq) if (f != 0) return false;
    return true;
}
```

5

# Linked Lists

### Node Structure

C++Copy

```cpp
struct ListNode {
    int val;
    ListNode* next;
    ListNode(int x) : val(x), next(nullptr) {}
};

// Doubly Linked List Node
struct DListNode {
    int val;
    DListNode *prev, *next;
    DListNode(int x) : val(x), prev(nullptr), next(nullptr) {}
};
```

### Pattern 1: Fast and Slow Pointer (Floyd's Tortoise and Hare)

#### Intuition

Two pointers move at different speeds. _Slow_ moves 1 step, _fast_ moves 2 steps. If there's a cycle, fast will eventually lap slow (like runners on a circular track). If no cycle, fast reaches the end. This same technique finds the **middle node**: when fast reaches the end, slow is at the middle.

C++Copy

```cpp
// Find Middle of Linked List
ListNode* middleNode(ListNode* head) {
    ListNode *slow = head, *fast = head;
    while (fast && fast->next) {
        slow = slow->next;
        fast = fast->next->next;
    }
    return slow;
}

// Detect Cycle (Floyd's Algorithm)
bool hasCycle(ListNode* head) {
    ListNode *slow = head, *fast = head;
    while (fast && fast->next) {
        slow = slow->next;
        fast = fast->next->next;
        if (slow == fast) return true;
    }
    return false;
}

// Find Start of Cycle
ListNode* detectCycleStart(ListNode* head) {
    ListNode *slow = head, *fast = head;
    while (fast && fast->next) {
        slow = slow->next;
        fast = fast->next->next;
        if (slow == fast) {
            // Move one pointer to head, both move 1 step
            slow = head;
            while (slow != fast) {
                slow = slow->next;
                fast = fast->next;
            }
            return slow;
        }
    }
    return nullptr;
}

// Palindrome Linked List — O(1) space
bool isPalindrome(ListNode* head) {
    // Find middle
    ListNode *slow = head, *fast = head;
    while (fast && fast->next) {
        slow = slow->next;
        fast = fast->next->next;
    }
    // Reverse second half
    ListNode *prev = nullptr;
    while (slow) {
        ListNode* tmp = slow->next;
        slow->next = prev;
        prev = slow;
        slow = tmp;
    }
    // Compare
    ListNode *left = head, *right = prev;
    while (right) {
        if (left->val != right->val) return false;
        left = left->next;
        right = right->next;
    }
    return true;
}
```

### Pattern 2: In-place Reversal

C++Copy

```cpp
// Reverse Linked List — Iterative
ListNode* reverseList(ListNode* head) {
    ListNode *prev = nullptr, *curr = head;
    while (curr) {
        ListNode* nxt = curr->next;
        curr->next = prev;
        prev = curr;
        curr = nxt;
    }
    return prev;
}

// Reverse Between positions left and right (1-indexed)
ListNode* reverseBetween(ListNode* head, int left, int right) {
    ListNode dummy(0);
    dummy.next = head;
    ListNode* prev = &dummy;
    for (int i = 1; i < left; i++) prev = prev->next;

    ListNode* curr = prev->next;
    for (int i = 0; i < right - left; i++) {
        ListNode* nxt = curr->next;
        curr->next = nxt->next;
        nxt->next = prev->next;
        prev->next = nxt;
    }
    return dummy.next;
}

// Reverse Nodes in K-Group
ListNode* reverseKGroup(ListNode* head, int k) {
    // Check if k nodes available
    ListNode* check = head;
    for (int i = 0; i < k; i++) {
        if (!check) return head;
        check = check->next;
    }
    // Reverse k nodes
    ListNode *prev = nullptr, *curr = head;
    for (int i = 0; i < k; i++) {
        ListNode* nxt = curr->next;
        curr->next = prev;
        prev = curr;
        curr = nxt;
    }
    // head is now tail of reversed segment; connect to rest
    head->next = reverseKGroup(curr, k);
    return prev;
}
```

### Pattern 3: Merge

C++Copy

```cpp
// Merge Two Sorted Lists
ListNode* mergeTwoLists(ListNode* l1, ListNode* l2) {
    ListNode dummy(0);
    ListNode* tail = &dummy;
    while (l1 && l2) {
        if (l1->val <= l2->val) {
            tail->next = l1;
            l1 = l1->next;
        } else {
            tail->next = l2;
            l2 = l2->next;
        }
        tail = tail->next;
    }
    tail->next = l1 ? l1 : l2;
    return dummy.next;
}

// Merge K Sorted Lists — Divide and Conquer
ListNode* mergeKLists(vector<ListNode*>& lists) {
    if (lists.empty()) return nullptr;
    int n = lists.size();
    while (n > 1) {
        for (int i = 0; i < n / 2; i++)
            lists[i] = mergeTwoLists(lists[i], lists[n - 1 - i]);
        n = (n + 1) / 2;
    }
    return lists[0];
}
```

Time: O(N log k) where N = total nodes, k = number of lists. Space: O(1)

6

# Stack

### Monotonic Stack Pattern

#### Intuition

A monotonic stack maintains elements in strictly increasing or decreasing order. When a new element violates the order, pop elements until the invariant is restored. This is the secret weapon for _"next greater element"_, _"previous smaller element"_, _"stock span"_, and _"largest rectangle"_ problems.

#### When to Use

Whenever you see: "Find the next/previous greater/smaller element for every element in an array." This is almost always a monotonic stack problem.

C++Copy

```cpp
// Next Greater Element — Monotonic Decreasing Stack
vector<int> nextGreaterElement(vector<int>& nums) {
    int n = nums.size();
    vector<int> result(n, -1);
    stack<int> st; // stores indices

    for (int i = 0; i < n; i++) {
        while (!st.empty() && nums[st.top()] < nums[i]) {
            result[st.top()] = nums[i];
            st.pop();
        }
        st.push(i);
    }
    return result;
}

// Daily Temperatures — "How many days until a warmer temperature?"
vector<int> dailyTemperatures(vector<int>& temperatures) {
    int n = temperatures.size();
    vector<int> result(n, 0);
    stack<int> st;

    for (int i = 0; i < n; i++) {
        while (!st.empty() && temperatures[st.top()] < temperatures[i]) {
            int prev = st.top(); st.pop();
            result[prev] = i - prev;
        }
        st.push(i);
    }
    return result;
}

// Largest Rectangle in Histogram
int largestRectangleArea(vector<int>& heights) {
    stack<int> st;
    int maxArea = 0;
    int n = heights.size();

    for (int i = 0; i <= n; i++) {
        int curHeight = (i == n) ? 0 : heights[i];
        while (!st.empty() && curHeight < heights[st.top()]) {
            int h = heights[st.top()]; st.pop();
            int w = st.empty() ? i : i - st.top() - 1;
            maxArea = max(maxArea, h * w);
        }
        st.push(i);
    }
    return maxArea;
}

// Valid Parentheses
bool isValid(string s) {
    stack<char> st;
    for (char c : s) {
        if (c == '(' || c == '{' || c == '[')
            st.push(c);
        else {
            if (st.empty()) return false;
            char top = st.top(); st.pop();
            if ((c == ')' && top != '(') ||
                (c == '}' && top != '{') ||
                (c == ']' && top != '['))
                return false;
        }
    }
    return st.empty();
}

// Stock Span — How many consecutive previous days had price ≤ today's
vector<int> stockSpan(vector<int>& prices) {
    int n = prices.size();
    vector<int> span(n);
    stack<int> st;

    for (int i = 0; i < n; i++) {
        while (!st.empty() && prices[st.top()] <= prices[i])
            st.pop();
        span[i] = st.empty() ? (i + 1) : (i - st.top());
        st.push(i);
    }
    return span;
}
```

**Pattern Recognition:** If the problem involves finding relationships between elements and their _nearest_ larger/smaller neighbors, reach for a monotonic stack. Time complexity drops from O(n²) brute force to O(n).

7

# Queue

### Types of Queues

Type

C++ Container

Key Property

Queue

`queue<int>`

FIFO — First In First Out

Deque

`deque<int>`

Insert/remove from both ends in O(1)

Priority Queue

`priority_queue<int>`

Max-heap by default, top = largest

Circular Queue

Custom (array + modulo)

Wraps around when reaching capacity

C++Copy

```cpp
// Sliding Window Maximum — using Monotonic Deque
vector<int> maxSlidingWindow(vector<int>& nums, int k) {
    deque<int> dq; // stores indices, front = max of current window
    vector<int> result;

    for (int i = 0; i < nums.size(); i++) {
        // Remove elements outside the window
        while (!dq.empty() && dq.front() <= i - k)
            dq.pop_front();

        // Remove smaller elements from back (they'll never be max)
        while (!dq.empty() && nums[dq.back()] <= nums[i])
            dq.pop_back();

        dq.push_back(i);

        if (i >= k - 1)
            result.push_back(nums[dq.front()]);
    }
    return result;
}

// First Negative in Every Window of Size K
vector<int> firstNegative(vector<int>& nums, int k) {
    deque<int> negatives;
    vector<int> result;

    for (int i = 0; i < nums.size(); i++) {
        if (nums[i] < 0) negatives.push_back(i);
        if (i - (negatives.empty() ? i : negatives.front()) >= k)
            negatives.pop_front();
        if (i >= k - 1)
            result.push_back(negatives.empty() || negatives.front() < i - k + 1 ? 0 : nums[negatives.front()]);
    }
    return result;
}
```

8

# Hashing

### Core Concepts

Hash tables provide O(1) average-case lookup, insertion, and deletion. In C++, `unordered_map` and `unordered_set` use hash tables, while `map` and `set` use Red-Black Trees (O(log n)).

#### Collision Handling Strategies

Method

Description

Pros/Cons

Chaining

Each bucket is a linked list

Simple; degrades to O(n) with many collisions

Open Addressing

Probe for next empty slot (linear/quadratic probing)

Better cache; clustering issues

Double Hashing

Second hash function determines probe step

Reduces clustering; more complex

C++Copy

```cpp
// Longest Consecutive Sequence — O(n) using HashSet
int longestConsecutive(vector<int>& nums) {
    unordered_set<int> numSet(nums.begin(), nums.end());
    int longest = 0;

    for (int num : numSet) {
        // Only start counting from the beginning of a sequence
        if (!numSet.count(num - 1)) {
            int length = 1;
            while (numSet.count(num + length))
                length++;
            longest = max(longest, length);
        }
    }
    return longest;
}

// Subarray Sum Equals K — Prefix Sum + HashMap
int subarraySum(vector<int>& nums, int k) {
    unordered_map<int, int> prefixCount;
    prefixCount[0] = 1; // empty prefix
    int sum = 0, count = 0;

    for (int num : nums) {
        sum += num;
        if (prefixCount.count(sum - k))
            count += prefixCount[sum - k];
        prefixCount[sum]++;
    }
    return count;
}

// Group Anagrams
vector<vector<string>> groupAnagrams(vector<string>& strs) {
    unordered_map<string, vector<string>> groups;
    for (auto& s : strs) {
        string key = s;
        sort(key.begin(), key.end());
        groups[key].push_back(s);
    }
    vector<vector<string>> result;
    for (auto& [key, group] : groups)
        result.push_back(group);
    return result;
}
```

**Interview Gotcha:** `unordered_map` worst case is O(n) per operation (all keys hash to same bucket). If the interviewer asks about worst case, mention `map` (O(log n) guaranteed) or custom hash functions.

9

# Recursion

### The Three Pillars

1.  **Base Case:** The termination condition. Without it, infinite recursion → stack overflow.
2.  **Recursive Relation:** How to reduce the problem to a smaller subproblem.
3.  **Call Stack:** Each recursive call adds a frame. Stack depth = space complexity.

Recursion Tree — fibonacci(5): fib(5) / \\ fib(4) fib(3) / \\ / \\ fib(3) fib(2) fib(2) fib(1) / \\ / \\ / \\ fib(2) fib(1) fib(1) fib(0) fib(1) fib(0) / \\ fib(1) fib(0) Time: O(2^n) — exponential, many repeated subproblems Space: O(n) — max call stack depth

C++Copy

```cpp
// Generate All Subsequences — Power Set
void generateSubsequences(vector<int>& nums, int idx, vector<int>& current,
                           vector<vector<int>>& result) {
    if (idx == nums.size()) {
        result.push_back(current);
        return;
    }
    // Choice 1: Include nums[idx]
    current.push_back(nums[idx]);
    generateSubsequences(nums, idx + 1, current, result);
    current.pop_back();

    // Choice 2: Exclude nums[idx]
    generateSubsequences(nums, idx + 1, current, result);
}

// Tower of Hanoi
void towerOfHanoi(int n, char from, char to, char aux) {
    if (n == 0) return;
    towerOfHanoi(n - 1, from, aux, to);
    cout << "Move disk " << n << " from " << from << " to " << to << endl;
    towerOfHanoi(n - 1, aux, to, from);
}

// Power function — O(log n)
long long power(long long base, long long exp, long long mod) {
    long long result = 1;
    base %= mod;
    while (exp > 0) {
        if (exp & 1) result = result * base % mod;
        base = base * base % mod;
        exp >>= 1;
    }
    return result;
}
```

10

# Backtracking

### The Backtracking Framework

Backtracking is recursion with **pruning**. The general template is: _choose → explore → unchoose_. You make a choice, recurse on the reduced problem, then undo the choice to try the next option.

C++Copy

```cpp
// Generic Backtracking Template
void backtrack(State& state, vector<Result>& results) {
    if (isGoalReached(state)) {
        results.push_back(state);
        return;
    }
    for (auto& choice : getChoices(state)) {
        if (isValid(choice, state)) {
            makeChoice(choice, state);      // Choose
            backtrack(state, results);       // Explore
            undoChoice(choice, state);       // Unchoose
        }
    }
}
```

### N-Queens

C++Copy

```cpp
// N-Queens Problem
class NQueens {
    int n;
    vector<vector<string>> results;
    vector<bool> cols, diag1, diag2; // columns, main diagonals, anti-diagonals

public:
    vector<vector<string>> solveNQueens(int n) {
        this->n = n;
        cols.assign(n, false);
        diag1.assign(2 * n, false);
        diag2.assign(2 * n, false);
        vector<string> board(n, string(n, '.'));
        solve(0, board);
        return results;
    }

    void solve(int row, vector<string>& board) {
        if (row == n) {
            results.push_back(board);
            return;
        }
        for (int col = 0; col < n; col++) {
            if (cols[col] || diag1[row - col + n] || diag2[row + col])
                continue; // Prune
            board[row][col] = 'Q';
            cols[col] = diag1[row - col + n] = diag2[row + col] = true;
            solve(row + 1, board);
            board[row][col] = '.';
            cols[col] = diag1[row - col + n] = diag2[row + col] = false;
        }
    }
};
```

### Sudoku Solver

C++Copy

```cpp
// Sudoku Solver
bool solveSudoku(vector<vector<char>>& board) {
    for (int i = 0; i < 9; i++) {
        for (int j = 0; j < 9; j++) {
            if (board[i][j] != '.') continue;
            for (char c = '1'; c <= '9'; c++) {
                if (isValidPlacement(board, i, j, c)) {
                    board[i][j] = c;
                    if (solveSudoku(board)) return true;
                    board[i][j] = '.'; // Backtrack
                }
            }
            return false; // No valid digit — trigger backtrack
        }
    }
    return true; // All cells filled
}

bool isValidPlacement(vector<vector<char>>& board, int row, int col, char c) {
    for (int i = 0; i < 9; i++) {
        if (board[row][i] == c) return false;
        if (board[i][col] == c) return false;
        if (board[3*(row/3) + i/3][3*(col/3) + i%3] == c) return false;
    }
    return true;
}
```

### Subsets, Permutations, Combination Sum

C++Copy

```cpp
// Subsets (Power Set)
vector<vector<int>> subsets(vector<int>& nums) {
    vector<vector<int>> result;
    vector<int> current;
    function<void(int)> backtrack = [&](int start) {
        result.push_back(current);
        for (int i = start; i < nums.size(); i++) {
            current.push_back(nums[i]);
            backtrack(i + 1);
            current.pop_back();
        }
    };
    backtrack(0);
    return result;
}

// Permutations
vector<vector<int>> permute(vector<int>& nums) {
    vector<vector<int>> result;
    function<void(int)> backtrack = [&](int start) {
        if (start == nums.size()) {
            result.push_back(nums);
            return;
        }
        for (int i = start; i < nums.size(); i++) {
            swap(nums[start], nums[i]);
            backtrack(start + 1);
            swap(nums[start], nums[i]);
        }
    };
    backtrack(0);
    return result;
}

// Combination Sum — elements can be reused
vector<vector<int>> combinationSum(vector<int>& candidates, int target) {
    vector<vector<int>> result;
    vector<int> current;
    function<void(int, int)> backtrack = [&](int start, int remaining) {
        if (remaining == 0) { result.push_back(current); return; }
        if (remaining < 0) return;
        for (int i = start; i < candidates.size(); i++) {
            current.push_back(candidates[i]);
            backtrack(i, remaining - candidates[i]); // i, not i+1 (reuse)
            current.pop_back();
        }
    };
    backtrack(0, target);
    return result;
}
```

11

# Binary Search

### Two Paradigms

**1\. Search Space Binary Search:** Search for an element in a sorted array. The search space is the array itself.

**2\. Answer Space Binary Search (BS on Answer):** The answer lies in a range \[lo, hi\]. For each mid, check if mid is a valid answer. Shrink the range based on feasibility. This is the more powerful pattern.

C++Copy

```cpp
// Classic Binary Search
int binarySearch(vector<int>& nums, int target) {
    int lo = 0, hi = nums.size() - 1;
    while (lo <= hi) {
        int mid = lo + (hi - lo) / 2; // Prevent overflow
        if (nums[mid] == target) return mid;
        else if (nums[mid] < target) lo = mid + 1;
        else hi = mid - 1;
    }
    return -1;
}

// Lower Bound — first index where nums[i] >= target
int lowerBound(vector<int>& nums, int target) {
    int lo = 0, hi = nums.size();
    while (lo < hi) {
        int mid = lo + (hi - lo) / 2;
        if (nums[mid] < target) lo = mid + 1;
        else hi = mid;
    }
    return lo;
}

// Upper Bound — first index where nums[i] > target
int upperBound(vector<int>& nums, int target) {
    int lo = 0, hi = nums.size();
    while (lo < hi) {
        int mid = lo + (hi - lo) / 2;
        if (nums[mid] <= target) lo = mid + 1;
        else hi = mid;
    }
    return lo;
}
```

### Binary Search on Answer

#### Template

C++Copy

```cpp
// BS on Answer Template — Minimize the Maximum / Maximize the Minimum
int binarySearchOnAnswer(int lo, int hi) {
    int ans = -1;
    while (lo <= hi) {
        int mid = lo + (hi - lo) / 2;
        if (isFeasible(mid)) {
            ans = mid;
            hi = mid - 1; // Minimize: search lower
            // lo = mid + 1; // Maximize: search higher
        } else {
            lo = mid + 1; // or hi = mid - 1
        }
    }
    return ans;
}

// Koko Eating Bananas
int minEatingSpeed(vector<int>& piles, int h) {
    int lo = 1, hi = *max_element(piles.begin(), piles.end());
    int ans = hi;
    while (lo <= hi) {
        int mid = lo + (hi - lo) / 2;
        long long hours = 0;
        for (int p : piles) hours += (p + mid - 1) / mid; // ceil(p/mid)
        if (hours <= h) { ans = mid; hi = mid - 1; }
        else lo = mid + 1;
    }
    return ans;
}

// Aggressive Cows — Maximize minimum distance
bool canPlace(vector<int>& stalls, int cows, int minDist) {
    int count = 1, lastPos = stalls[0];
    for (int i = 1; i < stalls.size(); i++) {
        if (stalls[i] - lastPos >= minDist) {
            count++;
            lastPos = stalls[i];
            if (count == cows) return true;
        }
    }
    return false;
}

int aggressiveCows(vector<int>& stalls, int cows) {
    sort(stalls.begin(), stalls.end());
    int lo = 1, hi = stalls.back() - stalls[0], ans = 0;
    while (lo <= hi) {
        int mid = lo + (hi - lo) / 2;
        if (canPlace(stalls, cows, mid)) { ans = mid; lo = mid + 1; }
        else hi = mid - 1;
    }
    return ans;
}

// Allocate Books — Minimize the maximum pages allocated
bool canAllocate(vector<int>& books, int students, int maxPages) {
    int count = 1, curPages = 0;
    for (int pages : books) {
        if (pages > maxPages) return false;
        if (curPages + pages > maxPages) {
            count++;
            curPages = pages;
            if (count > students) return false;
        } else {
            curPages += pages;
        }
    }
    return true;
}

int allocateBooks(vector<int>& books, int students) {
    int lo = *max_element(books.begin(), books.end());
    int hi = accumulate(books.begin(), books.end(), 0);
    int ans = hi;
    while (lo <= hi) {
        int mid = lo + (hi - lo) / 2;
        if (canAllocate(books, students, mid)) { ans = mid; hi = mid - 1; }
        else lo = mid + 1;
    }
    return ans;
}
```

**Pattern Recognition:** If the problem says "minimize the maximum" or "maximize the minimum", it's almost certainly _Binary Search on Answer_. The feasibility check function is the key — design it to run in O(n).

12

# Two Pointers

### Intuition

Use two pointers when the brute force involves nested loops over a **sorted/structured** input. By moving pointers intelligently, you skip unnecessary comparisons and reduce O(n²) → O(n).

C++Copy

```cpp
// Pair Sum in Sorted Array
pair<int,int> pairSum(vector<int>& nums, int target) {
    int lo = 0, hi = nums.size() - 1;
    while (lo < hi) {
        int sum = nums[lo] + nums[hi];
        if (sum == target) return {lo, hi};
        else if (sum < target) lo++;
        else hi--;
    }
    return {-1, -1};
}

// Container With Most Water
int maxArea(vector<int>& height) {
    int lo = 0, hi = height.size() - 1, maxWater = 0;
    while (lo < hi) {
        int water = min(height[lo], height[hi]) * (hi - lo);
        maxWater = max(maxWater, water);
        if (height[lo] < height[hi]) lo++;
        else hi--;
    }
    return maxWater;
}

// 3Sum — Find all unique triplets summing to 0
vector<vector<int>> threeSum(vector<int>& nums) {
    sort(nums.begin(), nums.end());
    vector<vector<int>> result;
    for (int i = 0; i < (int)nums.size() - 2; i++) {
        if (i > 0 && nums[i] == nums[i-1]) continue; // Skip duplicates
        int lo = i + 1, hi = nums.size() - 1;
        while (lo < hi) {
            int sum = nums[i] + nums[lo] + nums[hi];
            if (sum == 0) {
                result.push_back({nums[i], nums[lo], nums[hi]});
                while (lo < hi && nums[lo] == nums[lo+1]) lo++;
                while (lo < hi && nums[hi] == nums[hi-1]) hi--;
                lo++; hi--;
            } else if (sum < 0) lo++;
            else hi--;
        }
    }
    return result;
}

// Remove Duplicates from Sorted Array — In-place
int removeDuplicates(vector<int>& nums) {
    if (nums.empty()) return 0;
    int slow = 0;
    for (int fast = 1; fast < nums.size(); fast++) {
        if (nums[fast] != nums[slow]) {
            slow++;
            nums[slow] = nums[fast];
        }
    }
    return slow + 1;
}
```

13

# Sliding Window

### Fixed Window Template

C++Copy

```cpp
// Fixed Window — Maximum Sum Subarray of Size K
int maxSumSubarray(vector<int>& nums, int k) {
    int windowSum = 0, maxSum = INT_MIN;
    for (int i = 0; i < nums.size(); i++) {
        windowSum += nums[i];
        if (i >= k) windowSum -= nums[i - k];
        if (i >= k - 1) maxSum = max(maxSum, windowSum);
    }
    return maxSum;
}
```

### Variable Window Template

C++Copy

```cpp
// Variable Window Template
// Find the longest/shortest subarray satisfying a condition
int variableWindow(vector<int>& nums) {
    int left = 0, ans = 0;
    // State variables (hash map, counts, etc.)
    for (int right = 0; right < nums.size(); right++) {
        // Add nums[right] to window state

        while (/* window is invalid */) {
            // Remove nums[left] from window state
            left++;
        }
        ans = max(ans, right - left + 1); // or min for shortest
    }
    return ans;
}

// Longest Substring Without Repeating Characters
int lengthOfLongestSubstring(string s) {
    unordered_map<char, int> lastSeen;
    int left = 0, maxLen = 0;
    for (int right = 0; right < s.size(); right++) {
        if (lastSeen.count(s[right]) && lastSeen[s[right]] >= left)
            left = lastSeen[s[right]] + 1;
        lastSeen[s[right]] = right;
        maxLen = max(maxLen, right - left + 1);
    }
    return maxLen;
}

// Minimum Window Substring
string minWindow(string s, string t) {
    unordered_map<char, int> need, have;
    for (char c : t) need[c]++;
    int required = need.size(), formed = 0;
    int left = 0, minLen = INT_MAX, minStart = 0;

    for (int right = 0; right < s.size(); right++) {
        have[s[right]]++;
        if (need.count(s[right]) && have[s[right]] == need[s[right]])
            formed++;

        while (formed == required) {
            if (right - left + 1 < minLen) {
                minLen = right - left + 1;
                minStart = left;
            }
            have[s[left]]--;
            if (need.count(s[left]) && have[s[left]] < need[s[left]])
                formed--;
            left++;
        }
    }
    return minLen == INT_MAX ? "" : s.substr(minStart, minLen);
}

// Fruits Into Baskets (at most 2 distinct types)
int totalFruit(vector<int>& fruits) {
    unordered_map<int, int> basket;
    int left = 0, maxFruits = 0;
    for (int right = 0; right < fruits.size(); right++) {
        basket[fruits[right]]++;
        while (basket.size() > 2) {
            basket[fruits[left]]--;
            if (basket[fruits[left]] == 0) basket.erase(fruits[left]);
            left++;
        }
        maxFruits = max(maxFruits, right - left + 1);
    }
    return maxFruits;
}
```

**Key Insight:** Fixed window → use when the window size is given. Variable window → use when you need to find the optimal window size. The left pointer only moves forward, making total time O(n) despite the while loop.

14

# Sorting

### Comparison Table

Algorithm

Best

Average

Worst

Space

Stable?

In-place?

Bubble Sort

O(n)

O(n²)

O(n²)

O(1)

Yes

Yes

Selection Sort

O(n²)

O(n²)

O(n²)

O(1)

No

Yes

Insertion Sort

O(n)

O(n²)

O(n²)

O(1)

Yes

Yes

Merge Sort

O(n log n)

O(n log n)

O(n log n)

O(n)

Yes

No

Quick Sort

O(n log n)

O(n log n)

O(n²)

O(log n)

No

Yes

Heap Sort

O(n log n)

O(n log n)

O(n log n)

O(1)

No

Yes

C++Copy

```cpp
// Merge Sort
void merge(vector<int>& arr, int l, int m, int r) {
    vector<int> left(arr.begin() + l, arr.begin() + m + 1);
    vector<int> right(arr.begin() + m + 1, arr.begin() + r + 1);
    int i = 0, j = 0, k = l;
    while (i < left.size() && j < right.size())
        arr[k++] = (left[i] <= right[j]) ? left[i++] : right[j++];
    while (i < left.size()) arr[k++] = left[i++];
    while (j < right.size()) arr[k++] = right[j++];
}

void mergeSort(vector<int>& arr, int l, int r) {
    if (l >= r) return;
    int m = l + (r - l) / 2;
    mergeSort(arr, l, m);
    mergeSort(arr, m + 1, r);
    merge(arr, l, m, r);
}

// Quick Sort with Random Pivot
int partition(vector<int>& arr, int lo, int hi) {
    int pivotIdx = lo + rand() % (hi - lo + 1);
    swap(arr[pivotIdx], arr[hi]);
    int pivot = arr[hi], i = lo;
    for (int j = lo; j < hi; j++) {
        if (arr[j] < pivot) swap(arr[i++], arr[j]);
    }
    swap(arr[i], arr[hi]);
    return i;
}

void quickSort(vector<int>& arr, int lo, int hi) {
    if (lo >= hi) return;
    int p = partition(arr, lo, hi);
    quickSort(arr, lo, p - 1);
    quickSort(arr, p + 1, hi);
}

// Heap Sort
void heapify(vector<int>& arr, int n, int i) {
    int largest = i, l = 2*i+1, r = 2*i+2;
    if (l < n && arr[l] > arr[largest]) largest = l;
    if (r < n && arr[r] > arr[largest]) largest = r;
    if (largest != i) {
        swap(arr[i], arr[largest]);
        heapify(arr, n, largest);
    }
}

void heapSort(vector<int>& arr) {
    int n = arr.size();
    for (int i = n/2 - 1; i >= 0; i--) heapify(arr, n, i);
    for (int i = n - 1; i > 0; i--) {
        swap(arr[0], arr[i]);
        heapify(arr, i, 0);
    }
}
```

**Interview Tip:** When asked "which sort is best?": _Merge Sort_ for stability and guaranteed O(n log n). _Quick Sort_ for average-case speed (in-place, cache-friendly). _Heap Sort_ for O(1) space and guaranteed O(n log n). C++ `std::sort` uses IntroSort (Quick Sort + Heap Sort + Insertion Sort).

15

# Trees

### Node Structure & Terminology

C++Copy

```cpp
struct TreeNode {
    int val;
    TreeNode *left, *right;
    TreeNode(int x) : val(x), left(nullptr), right(nullptr) {}
};
```

Term

Definition

Height

Edges from node to deepest leaf. Height of tree = height of root.

Depth

Edges from root to the node. Root depth = 0.

Degree

Number of children a node has.

Full Binary Tree

Every node has 0 or 2 children.

Complete Binary Tree

All levels filled except possibly the last, which is filled left to right.

Perfect Binary Tree

All internal nodes have 2 children, all leaves at same level.

### Traversals

C++Copy

```cpp
// Preorder (Root → Left → Right)
void preorder(TreeNode* root, vector<int>& result) {
    if (!root) return;
    result.push_back(root->val);
    preorder(root->left, result);
    preorder(root->right, result);
}

// Inorder (Left → Root → Right) — gives sorted order for BST
void inorder(TreeNode* root, vector<int>& result) {
    if (!root) return;
    inorder(root->left, result);
    result.push_back(root->val);
    inorder(root->right, result);
}

// Postorder (Left → Right → Root)
void postorder(TreeNode* root, vector<int>& result) {
    if (!root) return;
    postorder(root->left, result);
    postorder(root->right, result);
    result.push_back(root->val);
}

// Level Order (BFS)
vector<vector<int>> levelOrder(TreeNode* root) {
    vector<vector<int>> result;
    if (!root) return result;
    queue<TreeNode*> q;
    q.push(root);
    while (!q.empty()) {
        int size = q.size();
        vector<int> level;
        for (int i = 0; i < size; i++) {
            TreeNode* node = q.front(); q.pop();
            level.push_back(node->val);
            if (node->left) q.push(node->left);
            if (node->right) q.push(node->right);
        }
        result.push_back(level);
    }
    return result;
}

// Morris Inorder Traversal — O(1) space, O(n) time
vector<int> morrisInorder(TreeNode* root) {
    vector<int> result;
    TreeNode* curr = root;
    while (curr) {
        if (!curr->left) {
            result.push_back(curr->val);
            curr = curr->right;
        } else {
            TreeNode* pred = curr->left;
            while (pred->right && pred->right != curr)
                pred = pred->right;
            if (!pred->right) {
                pred->right = curr; // Create thread
                curr = curr->left;
            } else {
                pred->right = nullptr; // Remove thread
                result.push_back(curr->val);
                curr = curr->right;
            }
        }
    }
    return result;
}
```

### Classic Tree Problems

C++Copy

```cpp
// Height of Binary Tree
int height(TreeNode* root) {
    if (!root) return 0;
    return 1 + max(height(root->left), height(root->right));
}

// Diameter of Binary Tree (longest path between any two nodes)
int diameter(TreeNode* root, int& ans) {
    if (!root) return 0;
    int lh = diameter(root->left, ans);
    int rh = diameter(root->right, ans);
    ans = max(ans, lh + rh); // Path through this node
    return 1 + max(lh, rh);
}

// Check if Balanced
bool isBalanced(TreeNode* root) {
    return checkHeight(root) != -1;
}
int checkHeight(TreeNode* root) {
    if (!root) return 0;
    int lh = checkHeight(root->left);
    if (lh == -1) return -1;
    int rh = checkHeight(root->right);
    if (rh == -1) return -1;
    if (abs(lh - rh) > 1) return -1;
    return 1 + max(lh, rh);
}

// Lowest Common Ancestor
TreeNode* LCA(TreeNode* root, TreeNode* p, TreeNode* q) {
    if (!root || root == p || root == q) return root;
    TreeNode* left = LCA(root->left, p, q);
    TreeNode* right = LCA(root->right, p, q);
    if (left && right) return root;
    return left ? left : right;
}
```

16

# Binary Search Tree

**BST Property:** For every node, all values in the left subtree are smaller, and all values in the right subtree are larger. Inorder traversal of a BST produces sorted output.

C++Copy

```cpp
// Insert into BST
TreeNode* insertBST(TreeNode* root, int val) {
    if (!root) return new TreeNode(val);
    if (val < root->val) root->left = insertBST(root->left, val);
    else root->right = insertBST(root->right, val);
    return root;
}

// Delete from BST
TreeNode* deleteBST(TreeNode* root, int key) {
    if (!root) return nullptr;
    if (key < root->val) root->left = deleteBST(root->left, key);
    else if (key > root->val) root->right = deleteBST(root->right, key);
    else {
        if (!root->left) return root->right;
        if (!root->right) return root->left;
        // Find inorder successor (smallest in right subtree)
        TreeNode* succ = root->right;
        while (succ->left) succ = succ->left;
        root->val = succ->val;
        root->right = deleteBST(root->right, succ->val);
    }
    return root;
}

// Validate BST
bool isValidBST(TreeNode* root, long lo = LONG_MIN, long hi = LONG_MAX) {
    if (!root) return true;
    if (root->val <= lo || root->val >= hi) return false;
    return isValidBST(root->left, lo, root->val) &&
           isValidBST(root->right, root->val, hi);
}

// Kth Smallest Element
int kthSmallest(TreeNode* root, int k) {
    stack<TreeNode*> st;
    TreeNode* curr = root;
    while (curr || !st.empty()) {
        while (curr) { st.push(curr); curr = curr->left; }
        curr = st.top(); st.pop();
        if (--k == 0) return curr->val;
        curr = curr->right;
    }
    return -1;
}

// LCA in BST — O(h) using BST property
TreeNode* lcaBST(TreeNode* root, TreeNode* p, TreeNode* q) {
    if (p->val < root->val && q->val < root->val)
        return lcaBST(root->left, p, q);
    if (p->val > root->val && q->val > root->val)
        return lcaBST(root->right, p, q);
    return root;
}
```

17

# Heap / Priority Queue

### Key Facts

*   **Min Heap:** Parent ≤ children. Root = minimum.
*   **Max Heap:** Parent ≥ children. Root = maximum.
*   C++ `priority_queue<int>` is a **max-heap** by default.
*   For min-heap: `priority_queue<int, vector<int>, greater<int>>`
*   Insert: O(log n), Extract min/max: O(log n), Peek: O(1)

#### When to Use

Any problem involving "Top K", "Kth largest/smallest", "merge K sorted", or "median from stream".

C++Copy

```cpp
// K Largest Elements
vector<int> kLargest(vector<int>& nums, int k) {
    // Use min-heap of size k
    priority_queue<int, vector<int>, greater<int>> minHeap;
    for (int num : nums) {
        minHeap.push(num);
        if (minHeap.size() > k) minHeap.pop();
    }
    vector<int> result;
    while (!minHeap.empty()) {
        result.push_back(minHeap.top());
        minHeap.pop();
    }
    return result;
}

// Top K Frequent Elements
vector<int> topKFrequent(vector<int>& nums, int k) {
    unordered_map<int, int> freq;
    for (int n : nums) freq[n]++;

    // Min-heap of {frequency, element}
    priority_queue<pair<int,int>, vector<pair<int,int>>, greater<>> minHeap;
    for (auto& [val, cnt] : freq) {
        minHeap.push({cnt, val});
        if (minHeap.size() > k) minHeap.pop();
    }

    vector<int> result;
    while (!minHeap.empty()) {
        result.push_back(minHeap.top().second);
        minHeap.pop();
    }
    return result;
}

// Merge K Sorted Arrays
vector<int> mergeKSorted(vector<vector<int>>& arrays) {
    // {value, array_index, element_index}
    priority_queue<tuple<int,int,int>, vector<tuple<int,int,int>>, greater<>> minHeap;

    for (int i = 0; i < arrays.size(); i++)
        if (!arrays[i].empty())
            minHeap.push({arrays[i][0], i, 0});

    vector<int> result;
    while (!minHeap.empty()) {
        auto [val, arr, idx] = minHeap.top(); minHeap.pop();
        result.push_back(val);
        if (idx + 1 < arrays[arr].size())
            minHeap.push({arrays[arr][idx+1], arr, idx+1});
    }
    return result;
}

// Find Median from Data Stream
class MedianFinder {
    priority_queue<int> maxHeap; // left half
    priority_queue<int, vector<int>, greater<int>> minHeap; // right half
public:
    void addNum(int num) {
        maxHeap.push(num);
        minHeap.push(maxHeap.top());
        maxHeap.pop();
        if (minHeap.size() > maxHeap.size()) {
            maxHeap.push(minHeap.top());
            minHeap.pop();
        }
    }
    double findMedian() {
        if (maxHeap.size() > minHeap.size()) return maxHeap.top();
        return (maxHeap.top() + minHeap.top()) / 2.0;
    }
};
```

18

# Trie (Prefix Tree)

A Trie is a tree-like data structure for efficient storage and retrieval of strings. Each node represents a character, and paths from root to marked nodes form stored words. Lookup is O(L) where L = word length — independent of how many words are stored.

C++Copy

```cpp
// Trie Implementation
class Trie {
    struct TrieNode {
        TrieNode* children[26] = {};
        bool isEnd = false;
        int prefixCount = 0; // # words with this prefix
    };
    TrieNode* root;

public:
    Trie() : root(new TrieNode()) {}

    void insert(const string& word) {
        TrieNode* node = root;
        for (char c : word) {
            int idx = c - 'a';
            if (!node->children[idx])
                node->children[idx] = new TrieNode();
            node = node->children[idx];
            node->prefixCount++;
        }
        node->isEnd = true;
    }

    bool search(const string& word) {
        TrieNode* node = find(word);
        return node && node->isEnd;
    }

    bool startsWith(const string& prefix) {
        return find(prefix) != nullptr;
    }

    int countWordsWithPrefix(const string& prefix) {
        TrieNode* node = find(prefix);
        return node ? node->prefixCount : 0;
    }

private:
    TrieNode* find(const string& s) {
        TrieNode* node = root;
        for (char c : s) {
            int idx = c - 'a';
            if (!node->children[idx]) return nullptr;
            node = node->children[idx];
        }
        return node;
    }
};
```

Trie after inserting: "app", "apple", "apt", "bat" root / \\ a b | | p a / \\ | p t\* t\* | l | e\* \* = isEnd (complete word)

19

# Graphs

### Representations

C++Copy

```cpp
// Adjacency List (preferred for sparse graphs)
vector<vector<int>> adj(n);
adj[u].push_back(v); // directed edge u → v
adj[v].push_back(u); // add this for undirected

// Adjacency List with weights
vector<vector<pair<int,int>>> adj(n);
adj[u].push_back({v, weight});

// Adjacency Matrix (for dense graphs, n ≤ 1000)
vector<vector<int>> mat(n, vector<int>(n, 0));
mat[u][v] = 1; // or weight
```

### BFS — Breadth First Search

C++Copy

```cpp
// BFS from source — finds shortest path in unweighted graph
vector<int> bfs(int src, vector<vector<int>>& adj, int n) {
    vector<int> dist(n, -1);
    queue<int> q;
    dist[src] = 0;
    q.push(src);
    while (!q.empty()) {
        int u = q.front(); q.pop();
        for (int v : adj[u]) {
            if (dist[v] == -1) {
                dist[v] = dist[u] + 1;
                q.push(v);
            }
        }
    }
    return dist;
}

// Number of Islands — BFS/DFS on grid
int numIslands(vector<vector<char>>& grid) {
    int rows = grid.size(), cols = grid[0].size(), count = 0;
    int dx[] = {0,0,1,-1}, dy[] = {1,-1,0,0};
    for (int i = 0; i < rows; i++) {
        for (int j = 0; j < cols; j++) {
            if (grid[i][j] == '1') {
                count++;
                queue<pair<int,int>> q;
                q.push({i, j});
                grid[i][j] = '0';
                while (!q.empty()) {
                    auto [x, y] = q.front(); q.pop();
                    for (int d = 0; d < 4; d++) {
                        int nx = x+dx[d], ny = y+dy[d];
                        if (nx >= 0 && nx < rows && ny >= 0 && ny < cols && grid[nx][ny] == '1') {
                            grid[nx][ny] = '0';
                            q.push({nx, ny});
                        }
                    }
                }
            }
        }
    }
    return count;
}
```

### DFS — Depth First Search

C++Copy

```cpp
// DFS — Recursive
void dfs(int u, vector<vector<int>>& adj, vector<bool>& visited) {
    visited[u] = true;
    for (int v : adj[u]) {
        if (!visited[v]) dfs(v, adj, visited);
    }
}

// Connected Components
int countComponents(int n, vector<vector<int>>& adj) {
    vector<bool> visited(n, false);
    int count = 0;
    for (int i = 0; i < n; i++) {
        if (!visited[i]) {
            dfs(i, adj, visited);
            count++;
        }
    }
    return count;
}

// Cycle Detection — Undirected (DFS)
bool hasCycleUndirected(int u, int parent, vector<vector<int>>& adj, vector<bool>& visited) {
    visited[u] = true;
    for (int v : adj[u]) {
        if (!visited[v]) {
            if (hasCycleUndirected(v, u, adj, visited)) return true;
        } else if (v != parent) {
            return true; // Back edge → cycle
        }
    }
    return false;
}

// Cycle Detection — Directed (DFS with coloring)
// 0 = white (unvisited), 1 = gray (in stack), 2 = black (done)
bool hasCycleDirected(int u, vector<vector<int>>& adj, vector<int>& color) {
    color[u] = 1;
    for (int v : adj[u]) {
        if (color[v] == 1) return true; // Back edge
        if (color[v] == 0 && hasCycleDirected(v, adj, color)) return true;
    }
    color[u] = 2;
    return false;
}
```

20

# Advanced Graph Algorithms

### Topological Sort

C++Copy

```cpp
// Kahn's Algorithm (BFS-based Topological Sort)
vector<int> topoSortKahn(int n, vector<vector<int>>& adj) {
    vector<int> inDeg(n, 0);
    for (int u = 0; u < n; u++)
        for (int v : adj[u]) inDeg[v]++;

    queue<int> q;
    for (int i = 0; i < n; i++)
        if (inDeg[i] == 0) q.push(i);

    vector<int> order;
    while (!q.empty()) {
        int u = q.front(); q.pop();
        order.push_back(u);
        for (int v : adj[u]) {
            if (--inDeg[v] == 0) q.push(v);
        }
    }
    // If order.size() != n → cycle exists
    return order;
}

// DFS-based Topological Sort
void topoDFS(int u, vector<vector<int>>& adj, vector<bool>& visited, stack<int>& st) {
    visited[u] = true;
    for (int v : adj[u])
        if (!visited[v]) topoDFS(v, adj, visited, st);
    st.push(u);
}
```

### Dijkstra's Algorithm

C++Copy

```cpp
// Dijkstra — Shortest Path (non-negative weights)
vector<long long> dijkstra(int src, vector<vector<pair<int,int>>>& adj, int n) {
    vector<long long> dist(n, LLONG_MAX);
    priority_queue<pair<long long,int>, vector<pair<long long,int>>, greater<>> pq;
    dist[src] = 0;
    pq.push({0, src});

    while (!pq.empty()) {
        auto [d, u] = pq.top(); pq.pop();
        if (d > dist[u]) continue; // Skip outdated entries
        for (auto [v, w] : adj[u]) {
            if (dist[u] + w < dist[v]) {
                dist[v] = dist[u] + w;
                pq.push({dist[v], v});
            }
        }
    }
    return dist;
}
```

Time: O((V + E) log V) with binary heap. Space: O(V)

### Bellman-Ford

C++Copy

```cpp
// Bellman-Ford — handles negative weights, detects negative cycles
struct Edge { int u, v, w; };

vector<long long> bellmanFord(int src, int n, vector<Edge>& edges) {
    vector<long long> dist(n, LLONG_MAX);
    dist[src] = 0;
    for (int i = 0; i < n - 1; i++) {
        for (auto& [u, v, w] : edges) {
            if (dist[u] != LLONG_MAX && dist[u] + w < dist[v])
                dist[v] = dist[u] + w;
        }
    }
    // Check for negative cycle
    for (auto& [u, v, w] : edges) {
        if (dist[u] != LLONG_MAX && dist[u] + w < dist[v])
            throw runtime_error("Negative cycle detected");
    }
    return dist;
}
```

Time: O(V × E)

### Floyd-Warshall

C++Copy

```cpp
// Floyd-Warshall — All-pairs shortest path
void floydWarshall(vector<vector<long long>>& dist, int n) {
    // dist[i][j] initialized to edge weight or INF
    for (int k = 0; k < n; k++)
        for (int i = 0; i < n; i++)
            for (int j = 0; j < n; j++)
                if (dist[i][k] != LLONG_MAX && dist[k][j] != LLONG_MAX)
                    dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j]);
}
```

Time: O(V³) Space: O(V²)

### Minimum Spanning Tree

C++Copy

```cpp
// Kruskal's MST using DSU
struct DSU {
    vector<int> parent, rank_;
    DSU(int n) : parent(n), rank_(n, 0) { iota(parent.begin(), parent.end(), 0); }
    int find(int x) { return parent[x] == x ? x : parent[x] = find(parent[x]); }
    bool unite(int x, int y) {
        x = find(x); y = find(y);
        if (x == y) return false;
        if (rank_[x] < rank_[y]) swap(x, y);
        parent[y] = x;
        if (rank_[x] == rank_[y]) rank_[x]++;
        return true;
    }
};

int kruskalMST(int n, vector<tuple<int,int,int>>& edges) {
    sort(edges.begin(), edges.end()); // Sort by weight
    DSU dsu(n);
    int mstWeight = 0, edgeCount = 0;
    for (auto& [w, u, v] : edges) {
        if (dsu.unite(u, v)) {
            mstWeight += w;
            if (++edgeCount == n - 1) break;
        }
    }
    return mstWeight;
}

// Prim's MST
int primMST(int n, vector<vector<pair<int,int>>>& adj) {
    vector<bool> inMST(n, false);
    priority_queue<pair<int,int>, vector<pair<int,int>>, greater<>> pq;
    pq.push({0, 0}); // {weight, node}
    int mstWeight = 0;
    while (!pq.empty()) {
        auto [w, u] = pq.top(); pq.pop();
        if (inMST[u]) continue;
        inMST[u] = true;
        mstWeight += w;
        for (auto [v, wt] : adj[u])
            if (!inMST[v]) pq.push({wt, v});
    }
    return mstWeight;
}
```

21

# Greedy

### How to Identify Greedy Problems

**Greedy works when:** Making the locally optimal choice at each step leads to a globally optimal solution. Key signal: the problem has _optimal substructure_ and the _greedy choice property_ — you never need to reconsider past decisions.

C++Copy

```cpp
// Activity Selection — Maximum non-overlapping intervals
int activitySelection(vector<pair<int,int>>& activities) {
    sort(activities.begin(), activities.end(), [](auto& a, auto& b) {
        return a.second < b.second; // Sort by end time
    });
    int count = 1, lastEnd = activities[0].second;
    for (int i = 1; i < activities.size(); i++) {
        if (activities[i].first >= lastEnd) {
            count++;
            lastEnd = activities[i].second;
        }
    }
    return count;
}

// Jump Game — Can you reach the last index?
bool canJump(vector<int>& nums) {
    int maxReach = 0;
    for (int i = 0; i < nums.size(); i++) {
        if (i > maxReach) return false;
        maxReach = max(maxReach, i + nums[i]);
    }
    return true;
}

// Jump Game II — Minimum jumps to reach end
int jump(vector<int>& nums) {
    int jumps = 0, curEnd = 0, farthest = 0;
    for (int i = 0; i < nums.size() - 1; i++) {
        farthest = max(farthest, i + nums[i]);
        if (i == curEnd) {
            jumps++;
            curEnd = farthest;
        }
    }
    return jumps;
}

// Gas Station
int canCompleteCircuit(vector<int>& gas, vector<int>& cost) {
    int totalSurplus = 0, currentSurplus = 0, start = 0;
    for (int i = 0; i < gas.size(); i++) {
        totalSurplus += gas[i] - cost[i];
        currentSurplus += gas[i] - cost[i];
        if (currentSurplus < 0) {
            start = i + 1;
            currentSurplus = 0;
        }
    }
    return totalSurplus >= 0 ? start : -1;
}

// Minimum Number of Meeting Rooms
int minMeetingRooms(vector<vector<int>>& intervals) {
    vector<int> starts, ends;
    for (auto& i : intervals) {
        starts.push_back(i[0]);
        ends.push_back(i[1]);
    }
    sort(starts.begin(), starts.end());
    sort(ends.begin(), ends.end());
    int rooms = 0, maxRooms = 0, j = 0;
    for (int i = 0; i < starts.size(); i++) {
        if (starts[i] < ends[j]) rooms++;
        else j++;
        maxRooms = max(maxRooms, rooms);
    }
    return maxRooms;
}
```

22

# Dynamic Programming

DP is the most important topic for interviews. The core idea: if a problem has **overlapping subproblems** and **optimal substructure**, solve each subproblem once and store the result.

### The 4 Steps

1.  **Recursion:** Write the brute-force recursive solution.
2.  **Memoization:** Cache results of recursive calls (top-down).
3.  **Tabulation:** Convert to iterative bottom-up with a DP table.
4.  **Space Optimization:** Reduce the DP table dimensions if possible.

### Pattern: Fibonacci / Climbing Stairs

C++Copy

```cpp
// Climbing Stairs — All 4 approaches

// 1. Recursion — O(2^n) time
int climbRecursion(int n) {
    if (n <= 1) return 1;
    return climbRecursion(n-1) + climbRecursion(n-2);
}

// 2. Memoization — O(n) time, O(n) space
int climbMemo(int n, vector<int>& dp) {
    if (n <= 1) return 1;
    if (dp[n] != -1) return dp[n];
    return dp[n] = climbMemo(n-1, dp) + climbMemo(n-2, dp);
}

// 3. Tabulation — O(n) time, O(n) space
int climbTab(int n) {
    vector<int> dp(n + 1);
    dp[0] = dp[1] = 1;
    for (int i = 2; i <= n; i++)
        dp[i] = dp[i-1] + dp[i-2];
    return dp[n];
}

// 4. Space Optimized — O(n) time, O(1) space
int climbOptimized(int n) {
    int prev2 = 1, prev1 = 1;
    for (int i = 2; i <= n; i++) {
        int curr = prev1 + prev2;
        prev2 = prev1;
        prev1 = curr;
    }
    return prev1;
}
```

### Pattern: 0/1 Knapsack

C++Copy

```cpp
// 0/1 Knapsack — Tabulation + Space Optimization
int knapsack(vector<int>& wt, vector<int>& val, int W) {
    int n = wt.size();
    // Space optimized: only need previous row
    vector<int> prev(W + 1, 0);
    for (int i = 0; i < n; i++) {
        vector<int> curr(W + 1, 0);
        for (int w = 0; w <= W; w++) {
            curr[w] = prev[w]; // Don't take item i
            if (wt[i] <= w)
                curr[w] = max(curr[w], val[i] + prev[w - wt[i]]);
        }
        prev = curr;
    }
    return prev[W];
}

// Single-row optimization (iterate backwards)
int knapsack1D(vector<int>& wt, vector<int>& val, int W) {
    int n = wt.size();
    vector<int> dp(W + 1, 0);
    for (int i = 0; i < n; i++)
        for (int w = W; w >= wt[i]; w--)
            dp[w] = max(dp[w], val[i] + dp[w - wt[i]]);
    return dp[W];
}
```

### Pattern: Unbounded Knapsack / Coin Change

C++Copy

```cpp
// Coin Change — Minimum coins to make amount
int coinChange(vector<int>& coins, int amount) {
    vector<int> dp(amount + 1, INT_MAX);
    dp[0] = 0;
    for (int i = 1; i <= amount; i++) {
        for (int coin : coins) {
            if (coin <= i && dp[i - coin] != INT_MAX)
                dp[i] = min(dp[i], 1 + dp[i - coin]);
        }
    }
    return dp[amount] == INT_MAX ? -1 : dp[amount];
}

// Coin Change 2 — Number of ways to make amount
int change(int amount, vector<int>& coins) {
    vector<int> dp(amount + 1, 0);
    dp[0] = 1;
    for (int coin : coins)      // Iterate coins first → unbounded
        for (int i = coin; i <= amount; i++)
            dp[i] += dp[i - coin];
    return dp[amount];
}
```

### Pattern: Longest Increasing Subsequence (LIS)

C++Copy

```cpp
// LIS — O(n²) DP
int lisDP(vector<int>& nums) {
    int n = nums.size();
    vector<int> dp(n, 1);
    int ans = 1;
    for (int i = 1; i < n; i++) {
        for (int j = 0; j < i; j++)
            if (nums[j] < nums[i])
                dp[i] = max(dp[i], dp[j] + 1);
        ans = max(ans, dp[i]);
    }
    return ans;
}

// LIS — O(n log n) using patience sorting
int lisBinarySearch(vector<int>& nums) {
    vector<int> tails; // tails[i] = smallest tail of all increasing subsequences of length i+1
    for (int num : nums) {
        auto it = lower_bound(tails.begin(), tails.end(), num);
        if (it == tails.end()) tails.push_back(num);
        else *it = num;
    }
    return tails.size();
}
```

### Pattern: Longest Common Subsequence (LCS)

C++Copy

```cpp
// LCS — Space Optimized
int lcs(string& a, string& b) {
    int m = a.size(), n = b.size();
    vector<int> prev(n + 1, 0), curr(n + 1, 0);
    for (int i = 1; i <= m; i++) {
        for (int j = 1; j <= n; j++) {
            if (a[i-1] == b[j-1])
                curr[j] = prev[j-1] + 1;
            else
                curr[j] = max(prev[j], curr[j-1]);
        }
        prev = curr;
        fill(curr.begin(), curr.end(), 0);
    }
    return prev[n];
}
```

### Pattern: Grid DP

C++Copy

```cpp
// Unique Paths
int uniquePaths(int m, int n) {
    vector<int> dp(n, 1);
    for (int i = 1; i < m; i++)
        for (int j = 1; j < n; j++)
            dp[j] += dp[j-1];
    return dp[n-1];
}

// Minimum Path Sum
int minPathSum(vector<vector<int>>& grid) {
    int m = grid.size(), n = grid[0].size();
    vector<int> dp(n);
    dp[0] = grid[0][0];
    for (int j = 1; j < n; j++) dp[j] = dp[j-1] + grid[0][j];
    for (int i = 1; i < m; i++) {
        dp[0] += grid[i][0];
        for (int j = 1; j < n; j++)
            dp[j] = grid[i][j] + min(dp[j], dp[j-1]);
    }
    return dp[n-1];
}
```

### Pattern: Partition DP (MCM)

C++Copy

```cpp
// Matrix Chain Multiplication
int mcm(vector<int>& dims) {
    int n = dims.size() - 1;
    // dp[i][j] = min cost to multiply matrices i..j
    vector<vector<int>> dp(n, vector<int>(n, 0));
    for (int len = 2; len <= n; len++) {
        for (int i = 0; i <= n - len; i++) {
            int j = i + len - 1;
            dp[i][j] = INT_MAX;
            for (int k = i; k < j; k++) {
                int cost = dp[i][k] + dp[k+1][j] + dims[i]*dims[k+1]*dims[j+1];
                dp[i][j] = min(dp[i][j], cost);
            }
        }
    }
    return dp[0][n-1];
}
```

**DP Pattern Recognition:**

*   _"Count the number of ways"_ → DP (sum subproblems)
*   _"Find the minimum/maximum"_ → DP (min/max subproblems)
*   _"Is it possible?"_ → DP (boolean OR subproblems)
*   _Choices at each step + overlapping states_ → DP
*   _String matching / edit distance_ → 2D DP

23

# Bit Manipulation

### Essential Bit Operations

Operation

Expression

Description

Check ith bit

`(n >> i) & 1`

Returns 1 if bit i is set

Set ith bit

`n | (1 << i)`

Sets bit i to 1

Clear ith bit

`n & ~(1 << i)`

Sets bit i to 0

Toggle ith bit

`n ^ (1 << i)`

Flips bit i

Check odd/even

`n & 1`

1 = odd, 0 = even

Check power of 2

`n & (n-1) == 0`

True if n is power of 2

Count set bits

`__builtin_popcount(n)`

GCC built-in

Lowest set bit

`n & (-n)`

Isolates the rightmost 1

Remove lowest set bit

`n & (n-1)`

Turns off rightmost 1

### Key XOR Properties

*   a ^ a = 0 (self-cancellation)
*   a ^ 0 = a (identity)
*   XOR is commutative and associative

C++Copy

```cpp
// Single Number — every element appears twice except one
int singleNumber(vector<int>& nums) {
    int result = 0;
    for (int n : nums) result ^= n;
    return result;
}

// Missing Number — array of [0, n] with one missing
int missingNumber(vector<int>& nums) {
    int xorAll = nums.size();
    for (int i = 0; i < nums.size(); i++)
        xorAll ^= i ^ nums[i];
    return xorAll;
}

// Count Set Bits (Brian Kernighan's Algorithm)
int countSetBits(int n) {
    int count = 0;
    while (n) {
        n &= (n - 1); // Remove lowest set bit
        count++;
    }
    return count;
}

// Generate All Subsets using Bitmask
vector<vector<int>> subsetsViabit(vector<int>& nums) {
    int n = nums.size();
    vector<vector<int>> result;
    for (int mask = 0; mask < (1 << n); mask++) {
        vector<int> subset;
        for (int i = 0; i < n; i++)
            if (mask & (1 << i))
                subset.push_back(nums[i]);
        result.push_back(subset);
    }
    return result;
}
```

24

# Segment Tree

A Segment Tree is a binary tree where each leaf represents an array element, and each internal node stores the result of a merge operation (sum, min, max, etc.) of its children. Supports both **range queries** and **point updates** in O(log n).

C++Copy

```cpp
// Segment Tree — Range Sum Query with Point Update
class SegmentTree {
    vector<long long> tree;
    int n;

public:
    SegmentTree(vector<int>& arr) {
        n = arr.size();
        tree.resize(4 * n);
        build(arr, 1, 0, n - 1);
    }

    void build(vector<int>& arr, int node, int start, int end) {
        if (start == end) {
            tree[node] = arr[start];
            return;
        }
        int mid = (start + end) / 2;
        build(arr, 2*node, start, mid);
        build(arr, 2*node+1, mid+1, end);
        tree[node] = tree[2*node] + tree[2*node+1];
    }

    void update(int idx, int val, int node = 1, int start = 0, int end = -1) {
        if (end == -1) end = n - 1;
        if (start == end) {
            tree[node] = val;
            return;
        }
        int mid = (start + end) / 2;
        if (idx <= mid) update(idx, val, 2*node, start, mid);
        else update(idx, val, 2*node+1, mid+1, end);
        tree[node] = tree[2*node] + tree[2*node+1];
    }

    long long query(int l, int r, int node = 1, int start = 0, int end = -1) {
        if (end == -1) end = n - 1;
        if (r < start || end < l) return 0; // Out of range
        if (l <= start && end <= r) return tree[node]; // Completely in range
        int mid = (start + end) / 2;
        return query(l, r, 2*node, start, mid) +
               query(l, r, 2*node+1, mid+1, end);
    }
};
```

Build: O(n) Query/Update: O(log n) Space: O(4n)

25

# Fenwick Tree (Binary Indexed Tree)

A Fenwick Tree supports prefix sum queries and point updates in O(log n) with much less code than a Segment Tree. The key insight: use the lowest set bit of the index to determine the range each node is responsible for.

C++Copy

```cpp
// Fenwick Tree / BIT
class FenwickTree {
    vector<long long> bit;
    int n;

public:
    FenwickTree(int n) : n(n), bit(n + 1, 0) {}

    void update(int idx, int delta) {
        for (idx++; idx <= n; idx += idx & (-idx))
            bit[idx] += delta;
    }

    long long prefixSum(int idx) {
        long long sum = 0;
        for (idx++; idx > 0; idx -= idx & (-idx))
            sum += bit[idx];
        return sum;
    }

    long long rangeSum(int l, int r) {
        return prefixSum(r) - (l ? prefixSum(l - 1) : 0);
    }
};
```

### Segment Tree vs Fenwick Tree

Feature

Segment Tree

Fenwick Tree

Code Complexity

More (~40 lines)

Minimal (~15 lines)

Range Queries

Sum, Min, Max, GCD

Sum only (standard)

Range Updates

With lazy propagation

Possible but tricky

Space

4n

n+1

Constant Factor

Higher

Lower (faster in practice)

26

# Complete Pattern Recognition Guide

This is the most important section for interviews. When you see a problem, match its characteristics to a known pattern below:

Problem Clue / Keywords

Pattern to Use

Key Data Structure

Sorted array, search target

Binary Search

Array

"Minimize the maximum" / "Maximize the minimum"

Binary Search on Answer

Array

Contiguous subarray sum/product

Sliding Window / Prefix Sum

Array / HashMap

"Longest substring with condition"

Sliding Window (Variable)

HashMap

Pair sum in sorted array

Two Pointers

Array

"Find all triplets/pairs"

Two Pointers / Sorting

Array

Linked list cycle / middle

Fast & Slow Pointer

Linked List

"Next greater / smaller element"

Monotonic Stack

Stack

Largest rectangle / histogram

Monotonic Stack

Stack

Matching brackets / expressions

Stack

Stack

Sliding window maximum

Monotonic Deque

Deque

"Top K" / "K-th largest"

Heap

Priority Queue

Merge K sorted

Heap

Priority Queue

Frequency / lookup

Hashing

HashMap / HashSet

Prefix / autocomplete / dictionary

Trie

Trie

Shortest path (unweighted)

BFS

Queue

Shortest path (weighted, no negatives)

Dijkstra

Min-Heap

Shortest path (negative weights)

Bellman-Ford

Edge List

All-pairs shortest path

Floyd-Warshall

2D Array

Connected components / islands

DFS / BFS / DSU

Graph

Cycle detection

DFS (coloring)

Graph

Prerequisites / ordering

Topological Sort

DAG

Minimum spanning tree

Kruskal / Prim

DSU / Heap

Connectivity queries

Disjoint Set Union

DSU

"Generate all" / "find all combinations"

Backtracking

Recursion

N-Queens / Sudoku

Backtracking

Recursion

Overlapping subproblems + optimal substructure

Dynamic Programming

Array / Table

"Count ways" / "min cost"

Dynamic Programming

Array / Table

Longest subsequence

DP (LIS / LCS)

Array

Knapsack / subset sum

DP (Knapsack)

1D/2D Array

Grid path counting

DP (Grid)

2D Array

Range sum / range update queries

Segment Tree / Fenwick

Tree

XOR tricks, single number

Bit Manipulation

Bitwise ops

Local optimal → global optimal

Greedy

Sorting

27

# Blind 75 Revision Checklist

### Arrays & Hashing

*    Two Sum Easy
*    Best Time to Buy and Sell Stock Easy
*    Contains Duplicate Easy
*    Product of Array Except Self Medium
*    Maximum Subarray Medium
*    Maximum Product Subarray Medium
*    Find Minimum in Rotated Sorted Array Medium
*    Search in Rotated Sorted Array Medium
*    3Sum Medium
*    Container With Most Water Medium

### Two Pointers & Sliding Window

*    Valid Palindrome Easy
*    Longest Substring Without Repeating Characters Medium
*    Longest Repeating Character Replacement Medium
*    Minimum Window Substring Hard

### Linked List

*    Reverse Linked List Easy
*    Merge Two Sorted Lists Easy
*    Linked List Cycle Easy
*    Remove Nth Node From End Medium
*    Reorder List Medium
*    Merge K Sorted Lists Hard

### Trees

*    Maximum Depth of Binary Tree Easy
*    Same Tree Easy
*    Invert Binary Tree Easy
*    Subtree of Another Tree Easy
*    Binary Tree Level Order Traversal Medium
*    Validate BST Medium
*    Kth Smallest Element in BST Medium
*    LCA of BST Medium
*    Construct Tree from Preorder & Inorder Medium
*    Binary Tree Maximum Path Sum Hard
*    Serialize / Deserialize Binary Tree Hard

### Graphs

*    Number of Islands Medium
*    Clone Graph Medium
*    Course Schedule Medium
*    Pacific Atlantic Water Flow Medium
*    Number of Connected Components Medium
*    Graph Valid Tree Medium

### Dynamic Programming

*    Climbing Stairs Easy
*    House Robber Medium
*    House Robber II Medium
*    Longest Increasing Subsequence Medium
*    Coin Change Medium
*    Longest Common Subsequence Medium
*    Word Break Medium
*    Combination Sum IV Medium
*    Unique Paths Medium
*    Decode Ways Medium

### Heap & Intervals

*    Merge Intervals Medium
*    Non-Overlapping Intervals Medium
*    Insert Interval Medium
*    Top K Frequent Elements Medium
*    Find Median From Data Stream Hard

### Bit Manipulation & Math

*    Sum of Two Integers Medium
*    Number of 1 Bits Easy
*    Counting Bits Easy
*    Missing Number Easy
*    Reverse Bits Easy

28

# Interview Revision Cheat Sheet

### Complexity Cheat Sheet

Data Structure

Access

Search

Insert

Delete

Array

O(1)

O(n)

O(n)

O(n)

Linked List

O(n)

O(n)

O(1)

O(1)

Stack/Queue

O(n)

O(n)

O(1)

O(1)

Hash Table

—

O(1)\*

O(1)\*

O(1)\*

BST (balanced)

O(log n)

O(log n)

O(log n)

O(log n)

Heap

O(1)†

O(n)

O(log n)

O(log n)

Trie

—

O(L)

O(L)

O(L)

\* = amortized average. † = peek only (min/max).

### Sorting Algorithms — Quick Reference

Algorithm

Best

Avg

Worst

Space

Stable

Merge Sort

O(n log n)

O(n log n)

O(n log n)

O(n)

✓

Quick Sort

O(n log n)

O(n log n)

O(n²)

O(log n)

✗

Heap Sort

O(n log n)

O(n log n)

O(n log n)

O(1)

✗

Counting Sort

O(n+k)

O(n+k)

O(n+k)

O(k)

✓

### Graph Algorithms — Quick Reference

Algorithm

Time

Space

Use Case

BFS

O(V+E)

O(V)

Shortest path (unweighted)

DFS

O(V+E)

O(V)

Components, cycle detection

Dijkstra

O((V+E)log V)

O(V)

Shortest path (positive weights)

Bellman-Ford

O(V×E)

O(V)

Negative weights

Floyd-Warshall

O(V³)

O(V²)

All-pairs shortest path

Kruskal

O(E log E)

O(V)

MST (sparse)

Prim

O((V+E)log V)

O(V)

MST (dense)

Topological Sort

O(V+E)

O(V)

DAG ordering

### Important Formulas

Formula

Value

Sum 1..n

n(n+1)/2

Sum of squares 1²..n²

n(n+1)(2n+1)/6

Nodes in perfect binary tree (height h)

2^(h+1) - 1

Height of balanced binary tree (n nodes)

⌊log₂(n)⌋

Catalan number C(n)

C(2n,n)/(n+1)

nCr combinations

n! / (r! × (n-r)!)

Number of subsets

2^n

Number of subsequences

2^n

Number of permutations

n!

### Common Interview Traps

*   **Integer Overflow:** Use `long long` for products, sums of large numbers. `mid = lo + (hi-lo)/2` instead of `(lo+hi)/2`.
*   **Off-by-one:** Check < vs <=, array bounds, loop conditions.
*   **Empty input:** Always handle n=0 or empty strings/arrays.
*   **Negative numbers:** Kadane fails without proper initialization. XOR works on negatives.
*   **Modular arithmetic:** (a + b) % MOD is not (a%MOD + b%MOD) if it exceeds MOD. Use `((a%MOD) + (b%MOD)) % MOD`.
*   **Unordered containers:** Worst case O(n). In competitive programming, use custom hash or ordered containers.
*   **Passing by value:** Large vectors/strings should be passed by reference (`&`).
*   **Global state:** Not resetting visited arrays between test cases.

29

# C++ STL for Interviews

### Sequence Containers

Container

Key Operations

Time Complexity

When to Use

`vector<T>`

push\_back, pop\_back, \[\], at

O(1)\* push\_back, O(1) access

Default container. Dynamic array.

`deque<T>`

push\_front/back, pop\_front/back

O(1) both ends

When you need both-end insertion.

`list<T>`

insert, erase, splice

O(1) insert/delete (with iterator)

Frequent insert/delete in middle.

`array<T,N>`

\[\], at, fill

O(1) access

Fixed-size, stack-allocated.

### Associative Containers

Container

Underlying Structure

Key Operations

Time

`set<T>`

Red-Black Tree

insert, erase, find, lower\_bound

O(log n)

`multiset<T>`

Red-Black Tree

Same as set, allows duplicates

O(log n)

`map<K,V>`

Red-Black Tree

\[\], insert, find, lower\_bound

O(log n)

`unordered_set<T>`

Hash Table

insert, erase, find, count

O(1)\*

`unordered_map<K,V>`

Hash Table

\[\], insert, find, count

O(1)\*

### Container Adaptors

Container

Operations

Notes

`stack<T>`

push, pop, top, empty, size

LIFO. Default: deque-backed.

`queue<T>`

push, pop, front, back, empty

FIFO. Default: deque-backed.

`priority_queue<T>`

push, pop, top, empty

Max-heap. For min-heap: `greater<T>`

### Essential Algorithms

C++Copy

```cpp
// Sorting
sort(v.begin(), v.end());                          // Ascending
sort(v.begin(), v.end(), greater<int>());          // Descending
sort(v.begin(), v.end(), [](int a, int b) {        // Custom comparator
    return abs(a) < abs(b);
});

// Binary Search (on sorted container)
binary_search(v.begin(), v.end(), target);         // Returns bool
lower_bound(v.begin(), v.end(), target);           // Iterator to first >= target
upper_bound(v.begin(), v.end(), target);           // Iterator to first > target

// Permutations
next_permutation(v.begin(), v.end());              // Modifies in-place, returns bool
prev_permutation(v.begin(), v.end());

// Min/Max
*min_element(v.begin(), v.end());
*max_element(v.begin(), v.end());
auto [mn, mx] = minmax_element(v.begin(), v.end());

// Accumulate
int sum = accumulate(v.begin(), v.end(), 0);
long long prod = accumulate(v.begin(), v.end(), 1LL, multiplies<long long>());

// Other useful
reverse(v.begin(), v.end());
rotate(v.begin(), v.begin() + k, v.end());        // Left rotate by k
unique(v.begin(), v.end());                        // Remove consecutive dups
v.erase(unique(v.begin(), v.end()), v.end());      // Actually remove them
count(v.begin(), v.end(), target);
fill(v.begin(), v.end(), val);
iota(v.begin(), v.end(), 0);                      // Fill with 0,1,2,3...
partial_sum(v.begin(), v.end(), prefix.begin());   // Prefix sums
```

30

# Pattern-Based Master Table

Pattern

How to Identify

Template Sketch

Classic Problems

**Fast & Slow Pointer**

Linked list cycle, middle element, palindrome check

slow = slow.next; fast = fast.next.next

Linked List Cycle, Middle Node, Happy Number

**Sliding Window**

"Longest/shortest subarray/substring with condition"

Expand right, shrink left when invalid

Min Window Substring, Longest Without Repeats, Fruits

**Two Pointers**

Sorted array + pair/triplet, partitioning

lo = 0, hi = n-1; move based on comparison

Two Sum II, 3Sum, Container With Most Water

**Binary Search**

Sorted data, monotonic predicate

lo, hi, mid; check feasibility

Search Element, Koko Bananas, Allocate Books

**Monotonic Stack**

Next/previous greater/smaller element

Stack of indices; pop when current violates order

Next Greater Element, Largest Rectangle, Daily Temps

**Prefix Sum**

Range sum queries, subarray sum equals K

prefix\[i\] = prefix\[i-1\] + arr\[i\]; query = prefix\[r\] - prefix\[l-1\]

Subarray Sum K, Range Sum Query, Continuous Subarray Sum

**Greedy**

Local optimal = global optimal, intervals

Sort by end time/criteria; greedily select

Activity Selection, Jump Game, Gas Station

**Backtracking**

"Generate all", combinations, permutations, constraints

Choose → Explore → Unchoose

N-Queens, Sudoku, Subsets, Permutations

**DP — Fibonacci**

State depends on previous 1-2 states

dp\[i\] = dp\[i-1\] + dp\[i-2\]

Climbing Stairs, House Robber, Decode Ways

**DP — Knapsack**

Include/exclude items, weight capacity

dp\[w\] = max(dp\[w\], val\[i\] + dp\[w-wt\[i\]\])

0/1 Knapsack, Subset Sum, Partition Equal Subset

**DP — LIS**

Longest increasing/decreasing subsequence

dp\[i\] = max(dp\[j\]+1) for j<i, a\[j\]<a\[i\] or Binary Search

LIS, Russian Doll Envelopes

**DP — LCS**

Two strings, longest common subsequence/substring

dp\[i\]\[j\] = dp\[i-1\]\[j-1\]+1 if match, else max of neighbors

LCS, Edit Distance, Shortest Common Supersequence

**Trie**

Prefix search, autocomplete, dictionary

Node with 26 children + isEnd flag

Implement Trie, Word Search II, Autocomplete

**Heap / Top-K**

"K largest/smallest", running median

Min-heap of size K for K largest

Top K Frequent, Kth Largest, Merge K Sorted

**DSU / Union-Find**

Connectivity, components, dynamic "is connected?"

find with path compression + union by rank

Number of Provinces, Redundant Connection, MST

**BFS**

Shortest path unweighted, level-order, grid exploration

Queue; process level by level

Word Ladder, Number of Islands, Rotten Oranges

**DFS**

Components, paths, tree traversal, cycle detection

Recursive or stack-based

Connected Components, Path Sum, Clone Graph

**Topological Sort**

Prerequisites, ordering, dependency resolution

Kahn (BFS with in-degree) or DFS post-order

Course Schedule, Alien Dictionary, Build Order

**Final Advice:** In an interview, spend 5 minutes understanding the problem and identifying the pattern before writing code. 70% of the battle is recognizing which pattern to apply. The implementation is just mechanical after that.