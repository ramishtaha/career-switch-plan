# Week 01 Guide — Foundations + First Microservices

> **Dates:** Jul 27 — Aug 2 | **Days:** 1–7
> **DSA:** Arrays, Hashing, Two Pointers, Stack, Linked List
> **Spring Boot:** Project setup, JPA, validation, 2 microservices, API Gateway, Eureka, Circuit Breaker
> **DevOps:** Docker, Docker Compose, GitHub Actions CI
> **AI:** First LLM API call, /ai/generate endpoint

---

## Table of Contents
1. [DSA — Arrays, Hashing, Two Pointers, Stack, Linked List](#dsa)
2. [Spring Boot — Microservices Foundation](#spring-boot)
3. [DevOps — Docker & CI/CD](#devops)
4. [AI Integration — LLM API Calls](#ai-integration)
5. [Day-by-Day Task Mapping](#day-by-day)
6. [Interview Q&A for Week 1 Topics](#interview-qa)
7. [Resources](#resources)

---

<a id="dsa"></a>
## 1. DSA — Arrays, Hashing, Two Pointers, Stack, Linked List

### 1.1 Core Concepts

#### Arrays
An array is a contiguous block of memory storing elements of the same type. In Java, arrays are fixed-size (unlike Python lists or C++ vectors). Java also provides `ArrayList` (backed by a dynamic array) which is more commonly used in interview solutions.

**Key properties:**
- Random access in O(1) via index
- Insertion/deletion at end is O(1) amortized (for ArrayList)
- Insertion/deletion in the middle is O(n) due to shifting
- Cache-friendly due to contiguous memory layout

**When to use arrays:**
- You need O(1) random access by index
- You know the size upfront (or use ArrayList)
- You need to sort or binary search (requires contiguous memory)

#### Hashing (HashMap / HashSet)
A hash map stores key-value pairs. A hash set stores unique keys. Both use a hash function to map keys to array indices (buckets).

**How HashMap works internally (Java):**
1. Java HashMap uses an array of buckets (default 16, load factor 0.75)
2. Each bucket is a linked list (or red-black tree if bucket size > 8 and capacity > 64)
3. `hash(key)` = `(h = key.hashCode()) ^ (h >>> 16)` — spreads bits to reduce collisions
4. Bucket index = `hash & (n-1)` where n is array length (always power of 2 for fast modulo)
5. When size > capacity × load_factor, the array doubles and all entries are rehashed
6. Java 8+ converts linked list to red-black tree when a bucket has > 8 entries — improves worst-case from O(n) to O(log n)

**Complexity:**
| Operation | Average | Worst (before tree-ify) |
|----------|---------|-------------------------|
| get/put/remove | O(1) | O(log n) (Java 8+) |
| Iteration | O(n) | O(n) |

**When to use:**
- You need O(1) lookup by key
- Counting frequencies
- Detecting duplicates
- Caching/memoization

#### Two Pointers
A technique where two indices move through an array (often from different ends or at different speeds) to solve problems in O(n) time with O(1) space.

**Two pointer patterns:**
1. **Opposite ends (converging):** One pointer at start, one at end, move toward center. Used for: sorted two-sum, palindromes, container with most water, trapping rain water
2. **Same direction (fast/slow):** Both start at left. Fast moves faster. Used for: removing duplicates, sliding window (variant), cycle detection in linked lists
3. **Two arrays:** One pointer per array. Used for: merging sorted arrays, intersection of sorted arrays

**Key property:** Two pointers work only when the array has some ordering property (sorted, or the problem allows greedy movement based on comparison)

#### Stack
A Last-In-First-Out (LIFO) data structure. Java's `Deque` (used as `ArrayDeque`) is preferred over the legacy `Stack` class.

**Operations:**
| Operation | Time | Method (ArrayDeque) |
|----------|------|---------------------|
| Push | O(1) | `push(e)` or `addFirst(e)` |
| Pop | O(1) | `pop()` or `removeFirst()` |
| Peek | O(1) | `peek()` or `peekFirst()` |
| Size | O(1) | `size()` |

**When to use a stack:**
- Parsing nested structures (parentheses, HTML tags)
- Evaluating postfix expressions
- Undo/redo functionality
- Monotonic stack problems (next greater element, largest rectangle in histogram)
- DFS traversal (recursion uses the call stack implicitly)

**Monotonic stack:** A stack that maintains elements in increasing or decreasing order. When pushing, pop all elements that violate the order. This is a powerful pattern for "next greater/smaller element" problems.

#### Linked List
A data structure where each node contains data and a reference to the next node (singly linked) or to both next and previous nodes (doubly linked).

**Singly linked list node:**
```java
class ListNode {
    int val;
    ListNode next;
    ListNode(int x) { val = x; }
}
```

**Key operations:**
| Operation | Time | Notes |
|----------|------|-------|
| Access by index | O(n) | Must traverse from head |
| Insert at head | O(1) | Just update head pointer |
| Insert at tail | O(n) | Must traverse (or O(1) with tail pointer) |
| Delete node | O(n) | Need to find predecessor |
| Search | O(n) | Linear scan |

**Common patterns:**
1. **Dummy head node:** Create a `dummy` node pointing to head. Simplifies edge cases (deleting head, merging). `dummy.next` is the new head.
2. **Fast/slow pointers (Floyd's cycle detection):** Slow moves 1 step, fast moves 2 steps. If they meet, there's a cycle. If fast reaches null, no cycle.
3. **Two-pass techniques:** First pass to count length, second pass to perform operation.
4. **Reversal:** Iterate through nodes, flipping `next` pointers one at a time.

---

### 1.2 Key Patterns Summary

| Pattern | When to Use | Time | Space | Example Problems |
|---------|-------------|------|-------|------------------|
| Hash Map counting | Need frequency/lookup | O(n) | O(n) | Two Sum, Top K Frequent |
| Hash Set membership | Need to check existence | O(n) | O(n) | Contains Duplicate, Longest Consecutive |
| Two Pointers (opposite ends) | Sorted array, greedy movement | O(n) | O(1) | Two Sum II, Container With Most Water |
| Two Pointers (same direction) | In-place modification | O(n) | O(1) | Remove Duplicates, Move Zeroes |
| Stack (matching) | Nested/balanced structures | O(n) | O(n) | Valid Parentheses |
| Stack (monotonic) | Next greater/smaller | O(n) | O(n) | Daily Temperatures |
| Fast/slow pointers | Cycle detection, find middle | O(n) | O(1) | Linked List Cycle |
| Dummy node | Head manipulation edge cases | O(n) | O(1) | Reverse Linked List, Merge Two Lists |

---

### 1.3 DSA Problems — Full Solutions

#### Problem 1: Contains Duplicate (LeetCode 217)
**Difficulty:** Easy | **Pattern:** Hash Set

**Problem:** Given an integer array `nums`, return `true` if any value appears at least twice, or `false` if every element is distinct.

**Approach:** Use a HashSet. For each element, check if it's already in the set. If yes, return true. If we finish without finding a duplicate, return false.

**Complexity:** O(n) time, O(n) space

```java
class Solution {
    public boolean containsDuplicate(int[] nums) {
        Set<Integer> seen = new HashSet<>();
        for (int num : nums) {
            if (seen.contains(num)) {
                return true;  // Found a duplicate
            }
            seen.add(num);
        }
        return false;  // All elements are distinct
    }
}
```

**Key Insight:** The `contains()` + `add()` can be combined — `HashSet.add()` returns `false` if the element already exists:
```java
public boolean containsDuplicate(int[] nums) {
    Set<Integer> seen = new HashSet<>();
    for (int num : nums) {
        if (!seen.add(num)) return true;  // add() returns false if already present
    }
    return false;
}
```

**Interview follow-up:** "Can you do it in O(1) space?"
- Yes: Sort the array (O(n log n)), then check adjacent pairs. But this modifies the input and is slower.

---

#### Problem 2: Two Sum (LeetCode 1)
**Difficulty:** Easy | **Pattern:** Hash Map

**Problem:** Given an array of integers `nums` and an integer `target`, return indices of the two numbers that add up to target. Each input has exactly one solution.

**Approach:** For each element, compute `complement = target - nums[i]`. Check if complement exists in a hash map (value → index). If yes, return both indices. If no, add current element to map.

**Complexity:** O(n) time, O(n) space

```java
class Solution {
    public int[] twoSum(int[] nums, int target) {
        Map<Integer, Integer> map = new HashMap<>();  // value → index
        for (int i = 0; i < nums.length; i++) {
            int complement = target - nums[i];
            if (map.containsKey(complement)) {
                return new int[] { map.get(complement), i };
            }
            map.put(nums[i], i);
        }
        return new int[] {};  // No solution found (won't happen per problem guarantee)
    }
}
```

**Key Insight:** We add to the map AFTER checking, not before. This handles the case where `nums = [3,3]`, `target = 6` — the second 3 finds the first 3 in the map. If we added before checking, we'd incorrectly return the same index twice.

**Interview follow-up:** "What if the array is sorted?"
- Use two pointers (see Two Sum II below). O(n) time, O(1) space. But you'd lose the original indices (need to store them separately).

---

#### Problem 3: Valid Anagram (LeetCode 242)
**Difficulty:** Easy | **Pattern:** Hash Map (frequency counting)

**Problem:** Given two strings `s` and `t`, return `true` if `t` is an anagram of `s` (same characters with same frequencies).

**Approach:** Count character frequencies in `s`, then decrement for `t`. If all counts are zero at the end, they're anagrams.

**Complexity:** O(n) time, O(1) space (26 letters)

```java
class Solution {
    public boolean isAnagram(String s, String t) {
        if (s.length() != t.length()) return false;

        int[] count = new int[26];  // a-z
        for (char c : s.toCharArray()) count[c - 'a']++;
        for (char c : t.toCharArray()) count[c - 'a']--;

        for (int c : count) {
            if (c != 0) return false;
        }
        return true;
    }
}
```

**Key Insight:** Using an `int[26]` array instead of a HashMap is faster and simpler for lowercase letters. For Unicode, use a HashMap.

---

#### Problem 4: Group Anagrams (LeetCode 49)
**Difficulty:** Medium | **Pattern:** Hash Map (sorted key)

**Problem:** Given an array of strings, group the anagrams together. Return groups in any order.

**Approach:** For each string, sort its characters to create a canonical key. Anagrams produce the same sorted key. Use a HashMap: sorted key → list of original strings.

**Complexity:** O(n × k log k) time (n strings, each of length k), O(n × k) space

```java
class Solution {
    public List<List<String>> groupAnagrams(String[] strs) {
        Map<String, List<String>> map = new HashMap<>();

        for (String s : strs) {
            char[] chars = s.toCharArray();
            Arrays.sort(chars);
            String key = new String(chars);  // sorted string as key

            map.computeIfAbsent(key, k -> new ArrayList<>()).add(s);
        }

        return new ArrayList<>(map.values());
    }
}
```

**Key Insight:** `computeIfAbsent` is cleaner than checking `containsKey` then `put`. It creates the list lazily only if the key is new.

**Optimization:** Instead of sorting (O(k log k)), use character frequency count as the key (O(k)):
```java
String key = Arrays.toString(count);  // count is int[26]
```
This makes total time O(n × k) but the constant factor is higher due to string conversion. In practice, sorting is often faster for short strings.

---

#### Problem 5: Top K Frequent Elements (LeetCode 347)
**Difficulty:** Medium | **Pattern:** Bucket Sort / Hash Map

**Problem:** Given an integer array `nums` and an integer `k`, return the `k` most frequent elements.

**Approach 1 (Bucket Sort — O(n)):**
1. Count frequencies with a HashMap
2. Create an array of lists where index = frequency. `bucket[i]` contains all elements that appear `i` times
3. Iterate from highest frequency bucket downward, collecting elements until we have `k`

```java
class Solution {
    public int[] topKFrequent(int[] nums, int k) {
        // Step 1: Count frequencies
        Map<Integer, Integer> count = new HashMap<>();
        for (int num : nums) {
            count.put(num, count.getOrDefault(num, 0) + 1);
        }

        // Step 2: Bucket sort by frequency
        List<Integer>[] bucket = new List[nums.length + 1];
        for (int num : count.keySet()) {
            int freq = count.get(num);
            if (bucket[freq] == null) bucket[freq] = new ArrayList<>();
            bucket[freq].add(num);
        }

        // Step 3: Collect top k from highest frequency bucket
        List<Integer> result = new ArrayList<>();
        for (int i = bucket.length - 1; i >= 0 && result.size() < k; i--) {
            if (bucket[i] != null) {
                result.addAll(bucket[i]);
            }
        }

        return result.stream().mapToInt(i -> i).toArray();
    }
}
```

**Key Insight:** Bucket sort achieves O(n) by trading space for time. The maximum frequency is n (all elements same), so bucket array size is n+1.

**Approach 2 (PriorityQueue — O(n log k)):**
```java
class Solution {
    public int[] topKFrequent(int[] nums, int k) {
        Map<Integer, Integer> count = new HashMap<>();
        for (int num : nums) count.merge(num, 1, Integer::sum);

        // Min-heap of size k, ordered by frequency
        PriorityQueue<Integer> heap = new PriorityQueue<>(
            (a, b) -> count.get(a) - count.get(b)
        );

        for (int num : count.keySet()) {
            heap.offer(num);
            if (heap.size() > k) heap.poll();  // remove least frequent
        }

        int[] result = new int[k];
        for (int i = 0; i < k; i++) result[i] = heap.poll();
        return result;
    }
}
```

**When to use which:** Bucket sort is O(n) but uses O(n) extra space. Heap is O(n log k) and uses O(k) space. For interviews, bucket sort is the "clever" solution; heap is the practical one.

---

#### Problem 6: Products of Array Except Self (LeetCode 238)
**Difficulty:** Medium | **Pattern:** Prefix/Suffix Product

**Problem:** Given an integer array `nums`, return an array `answer` where `answer[i]` is the product of all elements except `nums[i]`. Must be O(n) and must not use division.

**Approach:** For each element, the product-except-self = (product of all elements to the left) × (product of all elements to the right). Compute prefix products left-to-right, then multiply by suffix products right-to-left.

**Complexity:** O(n) time, O(1) space (output array doesn't count)

```java
class Solution {
    public int[] productExceptSelf(int[] nums) {
        int n = nums.length;
        int[] answer = new int[n];

        // Prefix pass: answer[i] = product of all elements to the left of i
        answer[0] = 1;  // nothing to the left of index 0
        for (int i = 1; i < n; i++) {
            answer[i] = answer[i - 1] * nums[i - 1];
        }

        // Suffix pass: multiply by product of all elements to the right of i
        int suffix = 1;  // running product from the right
        for (int i = n - 1; i >= 0; i--) {
            answer[i] = answer[i] * suffix;
            suffix *= nums[i];  // update suffix for next element (to the left)
        }

        return answer;
    }
}
```

**Key Insight:** The trick is doing it in two passes without extra arrays. After the prefix pass, `answer[i]` holds the left product. The suffix pass multiplies each by the running right product and then updates it. The `suffix` variable tracks the product of everything we've seen from the right so far.

**Why no division?** Because if any element is 0, division fails. The problem is designed to test whether you can handle this without the "obvious" division approach.

---

#### Problem 7: Longest Consecutive Sequence (LeetCode 128)
**Difficulty:** Medium | **Pattern:** Hash Set

**Problem:** Given an unsorted array of integers, find the length of the longest consecutive elements sequence. Must be O(n).

**Approach:** Add all elements to a HashSet. For each element, check if it's the START of a sequence (i.e., `num - 1` is NOT in the set). If it's a start, count how many consecutive numbers follow. Track the max.

**Complexity:** O(n) time (each element is visited at most twice), O(n) space

```java
class Solution {
    public int longestConsecutive(int[] nums) {
        Set<Integer> set = new HashSet<>();
        for (int num : nums) set.add(num);

        int longest = 0;
        for (int num : set) {  // iterate over set to avoid duplicate work
            // Only start counting if num is the beginning of a sequence
            if (!set.contains(num - 1)) {  // num is a sequence start
                int length = 1;
                while (set.contains(num + length)) {
                    length++;
                }
                longest = Math.max(longest, length);
            }
        }
        return longest;
    }
}
```

**Key Insight:** The `if (!set.contains(num - 1))` check is crucial. It ensures we only start counting from the actual beginning of a sequence. Without it, we'd recount sequences for each element, making it O(n²). Each element is part of exactly one sequence, and we only count each sequence once from its start.

---

#### Problem 8: Valid Palindrome (LeetCode 125)
**Difficulty:** Easy | **Pattern:** Two Pointers (opposite ends)

**Problem:** Given a string, determine if it is a palindrome, considering only alphanumeric characters and ignoring case.

**Approach:** Two pointers from both ends. Skip non-alphanumeric characters. Compare characters (case-insensitive).

```java
class Solution {
    public boolean isPalindrome(String s) {
        int left = 0, right = s.length() - 1;
        while (left < right) {
            // Skip non-alphanumeric from left
            while (left < right && !Character.isLetterOrDigit(s.charAt(left))) left++;
            // Skip non-alphanumeric from right
            while (left < right && !Character.isLetterOrDigit(s.charAt(right))) right--;

            if (Character.toLowerCase(s.charAt(left)) != Character.toLowerCase(s.charAt(right))) {
                return false;
            }
            left++;
            right--;
        }
        return true;
    }
}
```

**Key Insight:** The inner while loops must also check `left < right` to avoid index out of bounds when the string is all non-alphanumeric.

---

#### Problem 9: Two Sum II (LeetCode 167)
**Difficulty:** Medium | **Pattern:** Two Pointers (opposite ends, sorted array)

**Problem:** Given a 1-indexed sorted array, find two numbers that add up to target. Return indices (1-based).

**Approach:** Left pointer at start, right pointer at end. If sum < target, move left rightward (increase sum). If sum > target, move right leftward (decrease sum).

```java
class Solution {
    public int[] twoSumII(int[] numbers, int target) {
        int left = 0, right = numbers.length - 1;
        while (left < right) {
            int sum = numbers[left] + numbers[right];
            if (sum == target) {
                return new int[] { left + 1, right + 1 };  // 1-indexed
            } else if (sum < target) {
                left++;  // need a larger sum
            } else {
                right--;  // need a smaller sum
            }
        }
        return new int[] {};  // not found
    }
}
```

**Key Insight:** This only works because the array is sorted. The sorted property guarantees that moving left increases the sum and moving right decreases it. Without sorting, two pointers don't work for this pattern.

---

#### Problem 10: 3Sum (LeetCode 15)
**Difficulty:** Medium | **Pattern:** Two Pointers + Sort

**Problem:** Find all unique triplets in the array that sum to 0.

**Approach:** Sort the array. Fix the first element, then use two pointers for the remaining two. Skip duplicates.

**Complexity:** O(n²) time, O(1) space (excluding output)

```java
class Solution {
    public List<List<Integer>> threeSum(int[] nums) {
        List<List<Integer>> result = new ArrayList<>();
        Arrays.sort(nums);

        for (int i = 0; i < nums.length - 2; i++) {
            // Skip duplicates for the first element
            if (i > 0 && nums[i] == nums[i - 1]) continue;

            int left = i + 1, right = nums.length - 1;
            while (left < right) {
                int sum = nums[i] + nums[left] + nums[right];
                if (sum == 0) {
                    result.add(Arrays.asList(nums[i], nums[left], nums[right]));
                    // Skip duplicates for second and third elements
                    while (left < right && nums[left] == nums[left + 1]) left++;
                    while (left < right && nums[right] == nums[right - 1]) right--;
                    left++;
                    right--;
                } else if (sum < 0) {
                    left++;
                } else {
                    right--;
                }
            }
        }
        return result;
    }
}
```

**Key Insight:** Skipping duplicates is done at three levels: (1) outer loop skips duplicate first elements, (2) inner loop skips duplicate second elements after finding a triplet, (3) inner loop skips duplicate third elements. Without duplicate skipping, you get duplicate triplets in the output.

---

#### Problem 11: Container With Most Water (LeetCode 11)
**Difficulty:** Medium | **Pattern:** Two Pointers (opposite ends, greedy)

**Problem:** Given an array where each element represents the height of a vertical line, find two lines that form a container that holds the most water.

**Approach:** Two pointers at both ends. Area = min(height[left], height[right]) × (right - left). Move the pointer at the shorter line inward (because moving the taller one can only decrease or maintain area — the height is limited by the shorter line, and the width is shrinking).

```java
class Solution {
    public int maxArea(int[] height) {
        int left = 0, right = height.length - 1;
        int maxArea = 0;
        while (left < right) {
            int area = Math.min(height[left], height[right]) * (right - left);
            maxArea = Math.max(maxArea, area);
            // Move the shorter line inward
            if (height[left] < height[right]) {
                left++;
            } else {
                right--;
            }
        }
        return maxArea;
    }
}
```

**Key Insight:** The greedy choice is correct because the area is limited by the shorter line. Moving the taller line can never increase the area (the height can't increase beyond the shorter line, and width decreases). Moving the shorter line is the only chance for a larger area.

---

#### Problem 12: Trapping Rain Water (LeetCode 42)
**Difficulty:** Hard | **Pattern:** Two Pointers (opposite ends)

**Problem:** Given an array of non-negative integers representing an elevation map, compute how much water can be trapped after raining.

**Approach (Two Pointers — O(n) time, O(1) space):**
Water trapped at any position = min(max_left, max_right) - height[i]. Use two pointers from both ends, tracking `leftMax` and `rightMax`. Process the side with the smaller max (because that side determines the water level for that position).

```java
class Solution {
    public int trap(int[] height) {
        if (height.length == 0) return 0;
        int left = 0, right = height.length - 1;
        int leftMax = 0, rightMax = 0;
        int water = 0;

        while (left < right) {
            if (height[left] < height[right]) {
                // Left side is lower — water level determined by leftMax
                if (height[left] >= leftMax) {
                    leftMax = height[left];  // new max, can't trap water here
                } else {
                    water += leftMax - height[left];  // trap water
                }
                left++;
            } else {
                // Right side is lower or equal — water level determined by rightMax
                if (height[right] >= rightMax) {
                    rightMax = height[right];
                } else {
                    water += rightMax - height[right];
                }
                right--;
            }
        }
        return water;
    }
}
```

**Key Insight:** We always process the side with the smaller height because that side's max is the bottleneck. If `leftMax < rightMax`, then the water at `left` is determined by `leftMax` (because the right side is guaranteed to be at least `rightMax`, which is >= `leftMax`). So we can safely add `leftMax - height[left]`.

**Alternative approach (Prefix max arrays — O(n) time, O(n) space):**
```java
public int trap(int[] height) {
    int n = height.length;
    int[] leftMax = new int[n], rightMax = new int[n];
    leftMax[0] = height[0];
    for (int i = 1; i < n; i++) leftMax[i] = Math.max(leftMax[i-1], height[i]);
    rightMax[n-1] = height[n-1];
    for (int i = n-2; i >= 0; i--) rightMax[i] = Math.max(rightMax[i+1], height[i]);

    int water = 0;
    for (int i = 0; i < n; i++) water += Math.min(leftMax[i], rightMax[i]) - height[i];
    return water;
}
```

---

#### Problem 13: Valid Parentheses (LeetCode 20)
**Difficulty:** Easy | **Pattern:** Stack (matching)

**Problem:** Given a string containing `()[]{}`, determine if it's valid (properly nested and closed).

**Approach:** Stack. Push opening brackets. On closing bracket, check if stack top matches. If yes, pop. If no, invalid.

```java
class Solution {
    public boolean isValid(String s) {
        Map<Character, Character> matching = new HashMap<>();
        matching.put(')', '(');
        matching.put(']', '[');
        matching.put('}', '{');

        Deque<Character> stack = new ArrayDeque<>();
        for (char c : s.toCharArray()) {
            if (matching.containsValue(c)) {  // opening bracket
                stack.push(c);
            } else if (matching.containsKey(c)) {  // closing bracket
                if (stack.isEmpty() || stack.pop() != matching.get(c)) {
                    return false;
                }
            }
        }
        return stack.isEmpty();  // all brackets must be closed
    }
}
```

**Key Insight:** The final check `return stack.isEmpty()` is critical. If the stack is not empty, it means there are unclosed opening brackets. The problem isn't just about matching — it's about every bracket being closed.

---

#### Problem 14: Min Stack (LeetCode 155)
**Difficulty:** Medium | **Pattern:** Stack (auxiliary)

**Problem:** Design a stack that supports push, pop, top, and retrieving the minimum element in O(1) time.

**Approach:** Use two stacks: one for values, one for the minimum at each state. When pushing, also push the current min to the min stack. When popping, pop both.

```java
class MinStack {
    private Deque<Integer> stack;
    private Deque<Integer> minStack;

    public MinStack() {
        stack = new ArrayDeque<>();
        minStack = new ArrayDeque<>();
    }

    public void push(int val) {
        stack.push(val);
        // Push the smaller of val and current min. If minStack empty, push val.
        int min = minStack.isEmpty() ? val : Math.min(val, minStack.peek());
        minStack.push(min);
    }

    public void pop() {
        stack.pop();
        minStack.pop();
    }

    public int top() {
        return stack.peek();
    }

    public int getMin() {
        return minStack.peek();
    }
}
```

**Key Insight:** The min stack mirrors the main stack's state at every level. Each entry in minStack represents "what is the minimum from the bottom of the stack up to this point?" When we pop, we restore the previous state's min.

---

#### Problem 15: Evaluate Reverse Polish Notation (LeetCode 150)
**Difficulty:** Medium | **Pattern:** Stack (evaluation)

**Problem:** Evaluate an expression in reverse polish notation (postfix). Valid operators: +, -, *, /. Division truncates toward zero.

**Approach:** Stack. Push operands. When encountering an operator, pop two, apply, push result. Note order: second pop is the first operand.

```java
class Solution {
    public int evalRPN(String[] tokens) {
        Deque<Integer> stack = new ArrayDeque<>();
        for (String token : tokens) {
            switch (token) {
                case "+":
                    stack.push(stack.pop() + stack.pop());
                    break;
                case "-":
                    int b = stack.pop(), a = stack.pop();
                    stack.push(a - b);  // order matters for subtraction
                    break;
                case "*":
                    stack.push(stack.pop() * stack.pop());
                    break;
                case "/":
                    int divisor = stack.pop(), dividend = stack.pop();
                    stack.push(dividend / divisor);  // order matters for division
                    break;
                default:
                    stack.push(Integer.parseInt(token));
            }
        }
        return stack.pop();
    }
}
```

**Key Insight:** For subtraction and division, the order of operands matters. The first pop is the right operand, the second pop is the left operand. For addition and multiplication, order doesn't matter.

---

#### Problem 16: Reverse Linked List (LeetCode 206)
**Difficulty:** Easy | **Pattern:** Linked List (iterative reversal)

**Problem:** Reverse a singly linked list.

**Approach (Iterative):** Traverse the list, reversing each `next` pointer. Keep track of `prev` (previous node), `curr` (current node), and `next` (temp to save next node before overwriting).

```java
class Solution {
    public ListNode reverseList(ListNode head) {
        ListNode prev = null;
        ListNode curr = head;
        while (curr != null) {
            ListNode next = curr.next;  // save next before overwriting
            curr.next = prev;           // reverse the pointer
            prev = curr;               // move prev forward
            curr = next;               // move curr forward
        }
        return prev;  // prev is the new head (old tail)
    }
}
```

**Key Insight:** The order of operations is critical: save `next` before overwriting `curr.next`. `prev` starts as null because the old head's `next` should point to null (it becomes the new tail). After the loop, `prev` points to the old tail (new head).

**Recursive approach:**
```java
public ListNode reverseList(ListNode head) {
    if (head == null || head.next == null) return head;
    ListNode reversed = reverseList(head.next);
    head.next.next = head;  // make the next node point back to current
    head.next = null;       // break the old forward link
    return reversed;
}
```

---

#### Problem 17: Merge Two Sorted Lists (LeetCode 21)
**Difficulty:** Easy | **Pattern:** Linked List (dummy node + two pointers)

**Problem:** Merge two sorted linked lists into one sorted list.

**Approach:** Use a dummy head node to handle the edge case of an empty result. Compare values at both pointers, attach the smaller one, advance that pointer. At the end, attach any remaining nodes.

```java
class Solution {
    public ListNode mergeTwoLists(ListNode list1, ListNode list2) {
        ListNode dummy = new ListNode(0);
        ListNode curr = dummy;

        while (list1 != null && list2 != null) {
            if (list1.val <= list2.val) {
                curr.next = list1;
                list1 = list1.next;
            } else {
                curr.next = list2;
                list2 = list2.next;
            }
            curr = curr.next;
        }

        // Attach remaining nodes (one of these is null)
        curr.next = (list1 != null) ? list1 : list2;

        return dummy.next;  // dummy.next is the real head
    }
}
```

**Key Insight:** The dummy node eliminates the need to handle the "first node" as a special case. Without it, you'd need an `if (result == null)` check each time you add a node. `dummy.next` always points to the true head of the merged list.

---

#### Problem 18: Linked List Cycle (LeetCode 141)
**Difficulty:** Easy | **Pattern:** Fast/slow pointers (Floyd's cycle detection)

**Problem:** Given a linked list, determine if it has a cycle (a node visited again by following `next`).

**Approach:** Slow pointer moves 1 step, fast pointer moves 2 steps. If there's a cycle, fast will eventually meet slow (they're moving at different speeds in a closed loop). If fast reaches null, there's no cycle.

```java
public class Solution {
    public boolean hasCycle(ListNode head) {
        ListNode slow = head;
        ListNode fast = head;
        while (fast != null && fast.next != null) {
            slow = slow.next;        // 1 step
            fast = fast.next.next;   // 2 steps
            if (slow == fast) return true;  // they meet → cycle
        }
        return false;  // fast reached null → no cycle
    }
}
```

**Key Insight:** The cycle detection is guaranteed to work. In a cycle of length k, after enough steps, the gap between fast and slow is a multiple of k. Since fast gains 1 step on slow per iteration, they'll meet within k iterations.

**Alternative (HashSet):** Store visited nodes in a HashSet. O(n) time, O(n) space. Simpler but uses more space.

---

### 1.4 DSA Common Mistakes to Avoid

1. **Off-by-one errors in two pointers:** Always double-check loop conditions (`<` vs `<=`) and pointer updates
2. **Forgetting to check empty input:** Always handle `nums.length == 0`, `head == null`, `s.isEmpty()` at the start
3. **Modifying the array while iterating:** If you need to modify, use a copy or iterate backwards
4. **Integer overflow:** `int * int` can overflow. Use `long` for intermediate calculations in product problems
5. **Stack overflow in recursive linked list solutions:** For very long lists, iterative is safer than recursive
6. **Confusing `==` and `.equals()` for Integer/String in HashSet:** Java autoboxing can cause `==` to fail for integers > 127. Always use `.equals()` or compare primitives

---

<a id="spring-boot"></a>
## 2. Spring Boot — Microservices Foundation

### 2.1 Project Setup (Day 1)

#### Prerequisites
- JDK 17 (LTS, required for Spring Boot 3.x)
- IntelliJ IDEA Community Edition (free)
- Maven 3.8+ (bundled with IntelliJ)
- Git

#### Creating the Project
Use Spring Initializr (start.spring.io) or IntelliJ's built-in Spring Initializr:

**Dependencies for Week 1:**
- Spring Web (REST APIs)
- Spring Data JPA (database access)
- H2 Database (in-memory for development)
- Spring Boot DevTools (hot reload)
- Validation (bean validation)
- Spring Cloud Gateway (API Gateway — added in Day 5)
- Spring Cloud Eureka (service discovery — added in Day 6)

#### Maven pom.xml — Key Sections
```xml
<parent>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-parent</artifactId>
    <version>3.3.2</version>  <!-- Use latest 3.x -->
</parent>

<dependencies>
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-web</artifactId>
    </dependency>
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-data-jpa</artifactId>
    </dependency>
    <dependency>
        <groupId>com.h2database</groupId>
        <artifactId>h2</artifactId>
        <scope>runtime</scope>
    </dependency>
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-validation</artifactId>
    </dependency>
    <dependency>
        <groupId>org.springframework.boot</groupId>
<dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-test</artifactId>
        <scope>test</scope>
    </dependency>
</dependencies>
```

#### Project Structure (Standard Spring Boot Layout)
```
product-service/
├── src/main/java/com/ramish/productservice/
│   ├── ProductServiceApplication.java   ← Main class with @SpringBootApplication
│   ├── controller/
│   │   └── ProductController.java       ← REST endpoints
│   ├── service/
│   │   └── ProductService.java            ← Business logic
│   ├── repository/
│   │   └── ProductRepository.java        ← JPA repository
│   ├── model/
│   │   └── Product.java                  ← JPA entity
│   ├── dto/
│   │   ├── ProductRequest.java           ← Request DTO
│   │   └── ProductResponse.java         ← Response DTO
│   └── exception/
│       └── GlobalExceptionHandler.java  ← @ControllerAdvice
├── src/main/resources/
│   └── application.yml                   ← Configuration
└── pom.xml
```

---

### 2.2 JPA Entity + Repository (Day 2)

#### Product Entity
```java
package com.ramish.productservice.model;

import jakarta.persistence.*;
import java.math.BigDecimal;
import java.time.LocalDateTime;

@Entity
@Table(name = "products")
public class Product {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false)
    private String name;

    @Column(nullable = false, precision = 10, scale = 2)
    private BigDecimal price;

    @Column(length = 1000)
    private String description;

    @Column(nullable = false, updatable = false)
    private LocalDateTime createdAt;

    @Column(nullable = false)
    private LocalDateTime updatedAt;

    @PrePersist
    protected void onCreate() {
        LocalDateTime now = LocalDateTime.now();
        this.createdAt = now;
        this.updatedAt = now;
    }

    @PreUpdate
    protected void onUpdate() {
        this.updatedAt = LocalDateTime.now();
    }

    // Constructors
    public Product() {}

    public Product(String name, BigDecimal price) {
        this.name = name;
        this.price = price;
    }

    // Getters and Setters (omitted for brevity — generate with IntelliJ)
    public Long getId() { return id; }
    public void setId(Long id) { this.id = id; }
    public String getName() { return name; }
    public void setName(String name) { this.name = name; }
    public BigDecimal getPrice() { return price; }
    public setPrice(BigDecimal price) { this.price = price; }
    public String getDescription() { return description; }
    public void setDescription(String description) { this.description = description; }
    public LocalDateTime getCreatedAt() { return createdAt; }
    public void setCreatedAt(LocalDateTime createdAt) { this.createdAt = createdAt; }
    public LocalDateTime getUpdatedAt() { return updatedAt; }
    public void setUpdatedAt(LocalDateTime updatedAt) { this.updatedAt = updatedAt; }
}
```

**Key annotations explained:**
- `@Entity`: Marks this class as a JPA entity (mapped to a database table)
- `@Table`: Specifies table name (optional, defaults to class name)
- `@Id` + `@GeneratedValue`: Primary key with auto-increment
- `@Column`: Customizes column properties (nullable, length, precision)
- `@PrePersist` / `@PreUpdate`: JPA lifecycle callbacks for audit timestamps

#### Product Repository
```java
package com.ramish.productservice.repository;

import com.ramish.productservice.model.Product;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface ProductRepository extends JpaRepository<Product, Long> {
    // JpaRepository provides: save(), findById(), findAll(), deleteById(), etc.
    // Add custom query methods here:

    List<Product> findByNameContainingIgnoreCase(String name);

    // Using @Query for custom JPQL
    // @Query("SELECT p FROM Product p WHERE p.price BETWEEN :min AND :max")
    // List<Product> findByPriceRange(@Param("min") BigDecimal min, @Param("max") BigDecimal max);
}
```

**Key Insight:** JpaRepository provides 18+ methods out of the box. You only add custom methods for queries that Spring Data can't derive from method names. `findByNameContainingIgnoreCase` is automatically translated to a SQL query by Spring Data JPA.

---

### 2.3 Service Layer + Controller (Day 2)

#### DTOs (Data Transfer Objects)
```java
package com.ramish.productservice.dto;

import jakarta.validation.constraints.*;
import java.math.BigDecimal;

public class ProductRequest {
    @NotBlank(message = "Name is required")
    @Size(min = 2, max = 100, message = "Name must be 2-100 characters")
    private String name;

    @NotNull(message = "Price is required")
    @DecimalMin(value = "0.01", message = "Price must be positive")
    private BigDecimal price;

    @Size(max = 1000, message = "Description too long")
    private String description;

    // Getters and setters...
    public String getName() { return name; }
    public void setName(String name) { this.name = name; }
    public BigDecimal getPrice() { return price; }
    public void setPrice(BigDecimal price) { this.price = price; }
    public String getDescription() { return description; }
    public void setDescription(String description) { this.description = description; }
}
```

```java
package com.ramish.productservice.dto;

import java.math.BigDecimal;
import java.time.LocalDateTime;

public class ProductResponse {
    private Long id;
    private String name;
    private BigDecimal price;
    private String description;
    private LocalDateTime createdAt;

    // Constructor for mapping from entity
    public ProductResponse(Product product) {
        this.id = product.getId();
        this.name = product.getName();
        this.price = product.getPrice();
        this.description = product.getDescription();
        this.createdAt = product.getCreatedAt();
    }

    // Getters...
    public Long getId() { return id; }
    public String getName() { return name; }
    public BigDecimal getPrice() { return price; }
    public String getDescription() { return description; }
    public LocalDateTime getCreatedAt() { return createdAt; }
}
```

#### Product Service
```java
package com.ramish.productservice.service;

import com.ramish.productservice.dto.ProductRequest;
import com.ramish.productservice.dto.ProductResponse;
import com.ramish.ProductService.model.Product;
import com.ramish.productservice.repository.ProductRepository;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;
import java.util.stream.Collectors;

@Service
public class ProductService {

    private final ProductRepository productRepository;

    // Constructor injection (recommended over @Autowired field injection)
    public ProductService(ProductRepository productRepository) {
        this.productRepository = productRepository;
    }

    @Transactional
    public ProductResponse createProduct(ProductRequest request) {
        Product product = new Product();
        product.setName(request.getName());
        product.setPrice(request.getPrice());
        product.setDescription(request.getDescription());

        Product saved = productRepository.save(product);
        return new ProductResponse(saved);
    }

    @Transactional(readOnly = true)
    public List<ProductResponse> getAllProducts() {
        return productRepository.findAll().stream()
            .map(ProductResponse::new)
            .collect(Collectors.toList());
    }

    @Transactional(readOnly = true)
    public ProductResponse getProductById(Long id) {
        Product product = productRepository.findById(id)
            .orElseThrow(() -> new ResourceNotFoundException("Product not found with id: " + id));
        return new ProductResponse(product);
    }
}
```

#### Custom Exception
```java
package com.ramish.productservice.exception;

import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.ResponseStatus;

@ResponseStatus(HttpStatus.NOT_FOUND)
public class ResourceNotFoundException extends RuntimeException {
    public ResourceNotFoundException(String message) {
        super(message);
    }
}
```

#### Global Exception Handler
```java
package com.ramish.productservice.exception;

import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.validation.FieldError;
import validation.FieldError;
import org.springframework.web.bind.MethodArgumentNotValidException;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.RestControllerAdvice;

import java.time.LocalDateTime;
import java.util.HashMap;
import java.util.Map;

@RestControllerAdvice
public class GlobalExceptionHandler {

    // Handle "resource not found"
    @ExceptionHandler(ResourceNotFoundException.class)
    public ResponseEntity<Map<String, Object>> handleNotFound(ResourceNotFoundException ex) {
        Map<String, Object> body = new HashMap<>();
        body.put("timestamp", LocalDateTime.now());
        body.put("status", HttpStatus.NOT_FOUND.value());
        body.put("error", "Not Found");
        body.put("message", ex.getMessage());
        return ResponseEntity.status(HttpStatus.NOT_FOUND).body(body);
    }

    // Handle validation errors
    @ExceptionHandler(MethodArgumentNotValidException.class)
    public ResponseEntity<Map<String, Object>> handleValidation(MethodArgumentNotValidException ex) {
        Map<String, Object> body = JSON.Map<String, Object>();
        body.put("timestamp", LocalDateTime.now());
        body.put("status", HttpStatus.BAD_REQUEST.value());
        body.put("error", "Validation Error");

        Map<String, String> errors = new HashMap<>();
        for (FieldError error : ex.getBindingResult().getFieldErrors()) {
            errors.put(error.getField(), error.getDefaultMessage());
        }
        body.put("errors", errors);
        return ResponseEntity.status(HttpStatus.BAD_REQUEST).body(body);
    }

    // Handle all other exceptions
    @ExceptionHandler(Exception.class)
    public ResponseEntity<Map<String, Object>> handleGeneric(Exception ex) {
        Map<String, Object> body = new HashMap<>();
        body.put("timestamp", LocalDateTime.now());
        body.put("status", HttpStatus.INTERNAL_SERVER_ERROR.value());
        body.put("error", "Internal Server Error");
        body.put("message", ex.getMessage());
        return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body(body);
    }
}
```

#### Product Controller
```java
package com.ramish.productservice.controller;

import com.ramish.productservice.dto.ProductRequest;
import securing a response in the body
import com.ramish.productservice.dto.ProductResponse;
import com.ramish.productservice.service.ProductService;
import jakarta.validation.Valid;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/products")
public class ProductController {

    private final ProductService productService;

    public ProductController(ProductService productService) {
        this.productService = productService;
    }

    @PostMapping
    public ResponseEntity<ProductResponse> createProduct(@Valid @RequestBody ProductRequest request) {
        ProductResponse response = productService.createProduct(request);
        return ResponseEntity.status(HttpStatus.CREATED).body(response);
    }

    @GetMapping
    public ResponseEntity<List<ProductResponse>> getAllProducts() {
        return ResponseEntity.ok(productService.getAllProducts());
    }

    @GetMapping("/{id}")
    public ResponseEntity<ProductResponse> getProductById(@PathVariable Long id) {
        return ResponseEntity.ok(productService.getProductById(id));
    }
}
```

**Key annotations explained:**
- `@RestController`: Combines `@Controller` + `@ResponseBody` — every method returns JSON directly
- `@RequestMapping("/api/products")`: Base path for all endpoints
- `@PostMapping` / `@GetMapping`: HTTP method mapping
- `@Valid`: Triggers bean validation on the request body
- `@RequestBody`: Binds JSON request body to Java object
- `@PathVariable`: Extracts path parameter (`/api/products/1` → `id = 1`)
- `@ResponseStatus(HttpStatus.CREATED)`: Sets 201 status code
- `ResponseEntity`: Full control over HTTP response (status + headers + body)

---

### 2.4 Application Configuration (application.yml)
```yaml
server:
  port: 8080

spring:
  application:
    name: product-service
  datasource:
    url: jdbc:h2:mem:productdb  # in-memory database
    driver-class-name: org.h2.Driver
    username: sa
    password:
  jpa:
    show-sql: true              # log SQL queries
    hibernate:
      ddl-auto: update          # auto-create/update tables
    properties:
      hibernate:
        format_sql: true
  h2:
    console:
      enabled: true             # H2 web console at /h2-console
      path: /h2-console

logging:
  level:
    com.ramish.productservice: DEBUG
    org.hibernate.SQL: DEBUG
```

---

### 2.5 Inter-Service Communication (Day 4)

When splitting into two microservices (Product Service + Category Service), Product Service needs to call Category Service to get category details.

#### Using RestTemplate (Simple, synchronous)
```java
package com.ramish.productservice.service;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;

@Service
public class CategoryClient {

    private final RestTemplate restTemplate;
    private final String categoryServiceUrl;

    public CategoryClient(RestTemplate restTemplate,
                          @Value("${services.category-service.url}") String categoryServiceUrl) {
        this.restTemplate = restTemplate;
        this.categoryServiceUrl = categoryServiceUrl;
    }

    public CategoryResponse getCategoryById(Long categoryId) {
        String url = categoryServiceUrl + "/api/categories/" + categoryId;
        return restTemplate.getForObject(url, CategoryResponse.class);
    }
}
```

**Configuration:**
```yaml
services:
  category-service:
    url: http://localhost:8081
```

#### RestTemplate Bean Configuration
```java
package com.ramish.productservice.config;

import org.springframework.boot.web.client.RestTemplateBuilder;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.web.client.RestTemplate;

import java.time.Duration;

@Configuration
public class RestTemplateConfig {

    @Bean
    public RestTemplate restTemplate(RestTemplateBuilder builder) {
        return builder
            .setConnectTimeout(Duration.ofSeconds(3))
            .setReadTimeout(Duration.ofSeconds(5))
            .build();
    }
}
```

---

### 2.6 API Gateway (Day 5) — Spring Cloud Gateway

#### Gateway Project (Separate Module)
Create a new Spring Boot project with Spring Cloud Gateway dependency:

```xml
<dependency>
    <groupId>org.springframework.cloud</groupId>
    <artifactId>spring-cloud-starter-gateway</artifactId>
</dependency>
```

#### Gateway Application Configuration
```yaml
server:
  port: 9000

spring:
  application:
    name: api-gateway
  cloud:
    gateway:
      routes:
        - id: product-service
          uri: http://localhost:8080
          predicates:
            - Path=/api/products/**
        - id: category-service
          uri: http://localhost:8081
          predicates:
            - Path=/api/categories/**
```

**How it works:** The gateway listens on port 9000. Any request to `/api/products/**` is forwarded to `http://localhost:8080`. Any request to `/api/categories/**` is forwarded to `http://localhost:8081`. The client only talks to the gateway, not the individual services.

---

### 2.7 Eureka Service Discovery (Day 6)

#### Eureka Server (Separate Module)
```xml
<dependency>
    <groupId>org.springframework.cloud</groupId>
    <artifactId>spring-cloud-starter-netflix-eureka-server</artifactId>
</dependency>
```

```java
package com.ramish.eurekaserver;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.cloud.netflix.eureka.server.EnableEurekaServer;

@SpringBootApplication
@EnableEurekaServer
public class EurekaServerApplication {
    public static void main(String[] args) {
        SpringApplication.run(EurekaServerApplication.class, args);
    }
}
```

```yaml
# Eureka Server application.yml
server:
  port: 8761

eureka:
  client:
    register-with-eureka: false  # Eureka server doesn't register itself
    fetch-registry: false        # Don't fetch registry (it IS the registry)
  instance:
    hostname: localhost
```

#### Registering Services with Eureka
Add to each service (Product Service, Category Service):
```xml
<dependency>
    <groupId>discovery</groupId>
    <artifactId>spring-cloud-starter-netflix-eureka-client</artifactId>
</dependency>
```

```yaml
# In each service's application.yml
eureka:
  client:
    service-url:
      defaultZone: http://localhost:8761/eureka/
  instance:
    prefer-ip-address: true
```

```java
// Main class annotation
@SpringBootApplication
@EnableDiscoveryClient
public class ProductServiceApplication { ... }
```

**How Eureka works:**
1. Each service registers with Eureka on startup (sends its URL + metadata)
2. Eureka maintains a registry of all services and their instances
3. When Service A needs to call Service B, it asks Eureka for Service B's address
4. Eureka returns the available instances; Service A can load-balance among them
5. Heartbeats: each service sends a heartbeat every 30 seconds; if missed, Eureka removes it

---

### 2.8 Circuit Breaker — Resilience4j (Day 7)

#### Dependency
```xml
<dependency>
    <groupId>org.springframework.cloud</groupId>
    <artifactId>spring-cloud-starter-circuitbreaker-resilience4j</artifactId>
</dependency>
```

#### Configuration
```yaml
resilience4j:
  circuitbreaker:
    configs:
      default:
        sliding-window-size: 10               # last 10 calls
        minimum-number-of-calls: 5            # need 5 calls before evaluating
        failure-rate-threshold: 50            # 50% failure → open circuit
        wait-duration-in-open-state: 10s      # wait 10s before trying again
        permitted-number-of-calls-in-half-open-state: 3  # 3 test calls in half-open
```

#### Usage
```java
import io.github.resilience4j.circuitbreaker.annotation.CircuitBreaker;

@Service
public class CategoryClient {

    @CircuitBreaker(name = "category-service", fallbackMethod = "fallbackCategory")
    public CategoryResponse getCategoryById(Long categoryId) {
        return restTemplate.getForObject(
            categoryServiceUrl + "/api/categories/" + categoryId,
            CategoryResponse.class
        );
    }

    // Fallback method must have the same signature + exception parameter
    public CategoryResponse fallbackCategory(Long categoryId, Exception ex) {
        return new CategoryResponse(categoryId, "Unknown Category", "Category service unavailable");
    }
}
```

**Circuit Breaker states:**
1. **CLOSED:** Normal operation. Calls go through. Failure rate tracked.
2. **OPEN:** Failure rate exceeded threshold. All calls fail fast (no network call). Fallback is returned.
3. **HALF_OPEN:** After wait duration, allow a few test calls. If they succeed, circuit closes. If they fail, circuit reopens.

**Why circuit breakers matter in banking systems:** When a downstream service (e.g., risk limits service) is down, you don't want to keep trying and timeout. The circuit breaker fails fast and returns a safe fallback (e.g., "limits check unavailable — reject trade" or "limits check unavailable — use cached limits").

---

<a id="devops"></a>
## 3. DevOps — Docker & CI/CD

### 3.1 Docker Fundamentals

Docker containerizes your application + its dependencies into a single, portable unit. "Build once, run anywhere."

**Key concepts:**
- **Image:** A read-only template with your app + OS + dependencies. Built from a Dockerfile.
- **Container:** A running instance of an image. Isolated process with its own filesystem, network, and processes.
- **Dockerfile:** A text file with instructions to build an image.
- **Docker Compose:** Tool for defining and running multi-container applications (e.g., app + database).

### 3.2 Dockerfile for Spring Boot

```dockerfile
# Stage 1: Build
FROM maven:3.9-eclipse-temurin-17 AS builder
WORKDIR /app
COPY pom.xml .
RUN mvn dependency:resolve   # cache dependencies separately for faster builds
COPY src ./src
RUN mvn package -DskipTests

# Stage 2: Run (smaller image, no Maven/SDK)
FROM eclipse-temurin:17-jre-alpine
WORKDIR /app
COPY --from=builder /app/target/*.jar app.jar
EXPOSE 8080
ENTRYPOINT ["java", "-jar", "app.jar"]
```

**Multi-stage build:** Stage 1 uses the full Maven image to compile. Stage 2 uses a minimal JRE image to run. This keeps the final image small (~200MB vs ~800MB).

### 3.3 Docker Compose for Multi-Service

```yaml
# docker-compose.yml
version: "3.9"

services:
  product-service:
    build: ./product-service
    ports:
      - "8080:8080"
    environment:
      - SPRING_DATASOURCE_URL=jdbc:postgresql://postgres:5432/productdb
      - SPRING_DATASOURCE_USERNAME=postgres
      - SPRING_DATASOURCE_PASSWORD=postgres
    depends_on:
      - postgres
    networks:
      - app-network

  category-service:
    build: ./category-service
    ports:
      - "8081:8081"
    environment:
      - SPRING_DATASOURCE_URL=jdbc:postgresql://postgres:5432/categorydb
      - SPRING_DATASOURCE_USERNAME=postgres
      - Spring_DATASOURCE_PASSWORD=postgres
    depends_on:
      - postgres
    networks:
      - app-network

  postgres:
    image: postgres:16-alpine
    environment:
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=postgres
      - POSTGRES_DB=productdb
    ports:
      - "5432:5432"
    volumes:
      - postgres-data:/var/lib/postgresql/data
    networks:
      - app-network

networks:
  app-network:
    driver: bridge

volumes:
  postgres-data:
```

**Key concepts:**
- `depends_on`: Waits for the dependent container to start (but NOT for it to be ready — use healthchecks for that)
- `networks`: Containers on the same network can reach each other by service name (e.g., `postgres` resolves to the Postgres container's IP)
- `volumes`: Persistent storage. Data survives container restarts.
- `ports`: `HOST:CONTAINER` format. `8080:8080` means port 8080 on your machine maps to 8080 in the container.

### 3.4 GitHub Actions CI Pipeline

```yaml
# .github/workflows/ci.yml
name: CI Pipeline

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Set up JDK 17
        uses: actions/setup-java@v4
        with:
          java-version: '17'
          distribution: 'temurin'
          cache: maven

      - name: Build with Maven
        run: mvn clean verify -B  # -B = batch mode (no interactive prompts)

      - name: Run tests
        run: mvn test
```

**How it works:**
1. On every push or PR to main, GitHub spins up an Ubuntu VM
2. Checks out your code
3. Installs JDK 17
4. Builds the project with Maven (`mvn clean verify` compiles + runs tests + packages)
5. If tests fail, the pipeline fails and the PR is blocked

---

<a id="ai-integration"></a>
## 4. AI Integration — LLM API Calls

### 4.1 Making Your First LLM API Call (Day 2)

The serverless inference endpoints on Vultr, DigitalOcean, and Heroku use the OpenAI-compatible API format. This means any code that works with OpenAI's API also works with these providers.

#### cURL (Verify the API works)
```bash
curl -X POST https://api.vultrinference.com/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -d '{
    "model": "zai-org/GLM-5.2-FP8",
    "messages": [
      {"role": "system", "content": "You are a helpful product description writer."},
      {"role": "user", "content": "Write a 2-sentence description for: Wireless Mouse, Electronics category"}
    ],
    "temperature": 0.7,
    "max_tokens": 100
  }'
```

#### Expected Response Structure
```json
{
  "id": "chatcmpl-abc123",
  "model": "zai-org/GLM-5.2-FP8",
  "choices": [
    {
      "index": 0,
      "message": {
        "role": "assistant",
        "content": "This premium wireless mouse offers seamless connectivity and ergonomic comfort..."
      },
      "finish_reason": "stop"
    }
  ],
  "usage": {
    "prompt_tokens": 25,
    "completion_tokens": 42,
    "total_tokens": 67
  }
}
```

### 4.2 Java HTTP Client for LLM Calls (Day 3)

#### LLM Configuration in application.yml
```yaml
ai:
  inference:
    base-url: ${AI_BASE_URL:https://api.vultrinference.com/v1}
    api-key: ${AI_API_KEY}  # from environment variable, never hardcode
    model: ${AI_MODEL:zai-org/GLM-5.2-FP8}
    temperature: 0.7
    max-tokens: 200
    timeout-seconds: 30
```

#### Configuration Properties Class
```java
package com.ramish.productservice.config;

import org.springframework.boot.context.properties.ConfigurationProperties;
import org.springframework.stereotype.Component;

@Component
@ConfigurationProperties(prefix = "ai.inference")
public class AiProperties {
    private String baseUrl;
    private String apiKey;
    private String model;
    private double temperature;
    private int maxTokens;
    private int timeoutSeconds;

    // Getters and setters...
    public String getBaseUrl() { return baseUrl; }
    public void setBaseUrl(String baseUrl) { this.baseUrl = baseUrl; }
    public String getApiKey() { return apiKey; }
    public void setApiKey(String apiKey) { this.apiKey = apiKey; }
    public String getModel() { return model; }
    public void setModel(String model) { this.model = model; }
    public double getTemperature() { return temperature; }
    public void setTemperature(double temperature) { this.temperature = temperature; }
    public int getMaxTokens() { return maxTokens; }
    public void setMaxTokens(int maxTokens) { this.maxTokens = maxTokens; }
    public int getTimeoutSeconds() { return timeoutSeconds; }
    public void setTimeoutSeconds(int timeoutSeconds) { this.timeoutSeconds = timeoutSeconds; }
}
```

#### AI Service Class
```java
package com.ramish.productservice.ai;

import com.ramish.productservice.config.AiProperties;
import org.springframework.http.*;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;

import java.util.List;
import java.util.Map;

@Service
public class LlmService {

    private final RestTemplate restTemplate;
    private final AiProperties aiProperties;

    public LlmService(RestTemplate restTemplate, AiProperties aiProperties) {
        this.restTemplate = restTemplate;
        this.aiProperties = aiProperties;
    }

    public String generateProductDescription(String productName, String categoryName) {
        String url = aiProperties.getBaseUrl() + "/chat/completions";

        Map<String, Object> requestBody = Map.of(
            "model", aiProperties.getModel(),
            "messages", List.of(
                Map.of("role", "system", "content",
                    "You are a product description writer for an e-commerce platform. Write concise, professional descriptions."),
                Map.of("role", "user", "content",
                    String.format("Write a 2-sentence product description for: %s (Category: %s)", productName, categoryName))
            ),
            "temperature", aiProperties.getTemperature(),
            "max_tokens", aiProperties.getMaxTokens()
        );

        HttpHeaders headers = new HttpHeaders();
        headers.setContentType(MediaType.APPLICATION_JSON);
        headers.setBearerAuth(aiProperties.getApiKey());

        HttpEntity<Map<String, Object>> entity = new HttpEntity<>(requestBody, headers);

        try {
            ResponseEntity<Map> response = restTemplate.postForEntity(url, entity, Map.class);
            if (response.getStatusCode().is2xxSuccessful() && response.getBody() != null) {
                List<Map<String, Object>> choices = (List<Map<String, Object>>) response.getBody().get("choices");
                if (choices != null && !choices.isEmpty()) {
                    Map<String, Object> message = (Map<String, Object>) choices.get(0).get("message");
                    return (String) message.get("content");
                }
            }
            return "Description unavailable";
        } catch (Exception e) {
            return "Description unavailable: " + e.getMessage();
        }
    }
}
```

### 4.3 AI Endpoint in Controller (Day 4)

```java
@RestController
@RequestMapping("/api/products")
public class ProductController {

    private final ProductService productService;
    private final LlmService llmService;

    public ProductController(ProductService productService, LlmService llmService) {
        this.productService = productService;
        this.llmService = llmService;
    }

    // ... existing endpoints ...

    @PostMapping("/{id}/generate-description")
    public ResponseEntity<Map<String, String>> generateDescription(@PathVariable Long id) {
        ProductResponse product = productService.getProductById(id);
        String description = llmService.generateProductDescription(
            product.getName(),
            "General"  // Will use category name once categories are linked
        );

        // Save the generated description
        productService.updateDescription(id, description);

        return ResponseEntity.ok(Map.of("description", description));
    }
}
```

---

<a id="interview-qa"></a>
## 5. Interview Q&A for Week 1 Topics

### DSA Interview Questions

**Q1: How does Java's HashMap handle collisions?**
A: Java HashMap uses separate chaining (linked lists). When two keys hash to the same bucket, they're stored in a linked list at that bucket index. In Java 8+, if a bucket's linked list exceeds 8 entries and the array capacity exceeds 64, the linked list is converted to a red-black tree for O(log n) lookup instead of O(n).

**Q2: When would you use a HashSet vs ArrayList?**
A: HashSet when you need O(1) membership testing and uniqueness. ArrayList when you need ordered access, duplicates allowed, and O(1) index-based access. HashSet uses more memory per element but is dramatically faster for `contains()`.

**Q3: Explain the two-pointer technique for sorted arrays.**
A: Place one pointer at each end. Compute sum. If sum < target, move the left pointer rightward to increase sum. If sum > target, move the right pointer leftward to decrease sum. This works because the array is sorted — moving left only increases and moving right only decreases. Time O(n), space O(1).

**Q4: What is a monotonic stack and when do you use it?**
A: A stack that maintains elements in monotonic (strictly increasing or decreasing) order. When pushing, pop all elements that violate the monotonic property. Used for "next greater element" type problems. For example, to find the next greater element for each array element in O(n), use a decreasing stack — when a new element is greater than the stack top, it's the "next greater" for the popped element.

**Q5: How do you detect a cycle in a linked list without extra space?**
A: Floyd's cycle detection (tortoise and hare). Slow pointer moves 1 step, fast pointer moves 2 steps. If there's a cycle, fast will eventually catch up to slow (since fast gains 1 step per iteration in a cycle of length k, they'll meet within k iterations). If fast reaches null, there's no cycle. Time O(n), space O1).

### Spring Boot Interview Questions

**Q6: What is @RestControllerAdvice and how does it differ from @ControllerAdvice?**
A: `@RestControllerAdvice` combines `@ControllerAdvice` + `@ResponseBody`. It's used for REST APIs where you want exception responses as JSON. `@ControllerAdvice` is for traditional MVC where you might return error view pages. In a REST API, always use `@RestControllerAdvice`.

**Q7: Explain the layers of a Spring Boot application.**
A: Controller (handles HTTP requests/responses) → Service (business logic, annotated with @Service, @Transactional) → Repository (data access, extends JpaRepository) → Entity (database mapping, @Entity). DTOs separate the API contract from the database model. This separation keeps layers testable and maintainable.

**Q8: What is the difference between @RequestParam and @PathVariable?**
A: `@PathVariable` extracts values from the URI path (`/api/products/5` → `id=5`). `@RequestParam` extracts query parameters (`/api/products?name=laptop` → `name=laptop`). Use @PathVariable for resource identifiers, @RequestParam for filters/options.

**Q9: Why use DTOs instead of returning entities directly?**
A: (1) Security — entities may contain fields you don't want to expose (e.g., internal IDs, audit fields). (2) API stability — you can change the entity schema without breaking the API contract. (3) Customization — you can compute derived fields in the DTO. (4) Prevents lazy loading issues — serializing an entity can trigger unexpected database queries.

**Q10: How does Eureka service discovery work?**
A: Each microservice registers with the Eureka server on startup, sending its service name, host, and port. Eureka maintains a registry. When Service A needs to call Service B, it queries Eureka for available instances of "service-b". Eureka returns the instance list. Service A can then load-balance (default: round-robin) across instances. Heartbeats every 30s keep registrations alive; if missed, Eureka evicts the instance.

### DevOps Interview Questions

**Q11: What is a Docker multi-stage build and why use it?**
A: Multi-stage builds use multiple FROM statements. The first stage compiles the app (needs Maven + JDK). The second stage only needs the JRE to run the compiled JAR. This reduces the final image from ~800MB to ~200MB, faster to pull and deploy, with a smaller attack surface.

**Q12: What's the difference between depends_on and healthchecks in Docker Compose?**
A: `depends_on` waits for a container to start, but not for it to be ready to accept connections. A healthcheck actively polls the service (e.g., `curl -f http://localhost:8080/actuator/health`) and only marks it as healthy when the check passes. Use healthchecks with `depends_on: condition: service_healthy` for correct startup ordering.

---

<a id="day-by-day"></a>
## 6. Day-by-Day Task Mapping

| Day | DSA Problems | Spring Boot Task | DevOps Task | AI Task |
|-----|-------------|-----------------|-------------|---------|
| 1 Mon | Contains Duplicate, Two Sum | Project setup, REST API, GitHub | Docker install | Explore inference dashboards |
| 2 Tue | Valid Anagram, Group Anagrams, Top K Frequent | JPA + H2 CRUD, exception handling | Dockerize app | First cURL API call |
| 3 Wed | Products of Array Except Self, Longest Consecutive | Validation, 2nd entity, One-to-Many | Docker Compose + Postgres | Java HTTP client, LLM description |
| 4 Thu | Valid Palindrome, Two Sum II, 3Sum | Split into 2 microservices, RestTemplate | Docker Compose 2 services | /ai/generate-description endpoint |
| 5 Fri | Container With Most Water, Trapping Rain Water | Spring Cloud Gateway | GitHub Actions CI | Configurable prompts |
| 6 Sat | Valid Parentheses, Min Stack, Evaluate RPN | Eureka Service Discovery | Provision DO Droplet | Multi-model comparison |
| 7 Sun | Reverse LL, Merge Two Sorted LL, LL Cycle | Resilience4j Circuit Breaker | Deploy to Droplet | Deploy AI endpoint + document |

---

<a id="resources"></a>
## 7. Resources

### DSA
- **NeetCode 150:** https://neetcode.io — Free, organized by pattern. Watch the approach video after trying for 20 min.
- **LeetCode:** https://leetcode.com — For solving problems. Filter by difficulty and topic.
- **Java visualizer:** https://csulearn.intellideas.org/ — Visualize data structures.
- **Big-O Cheatsheet:** https://www.bigocheatsheet.com/

### Spring Boot
- **Spring Academy:** https://spring.io/academy — Official, free tier available.
- **Spring Boot Reference:** https://docs.spring.io/spring-boot/docs/current/reference/html/
- **Baeldung:** https://www.baeldung.com — Excellent Spring Boot tutorials.
- **Spring Boot GitHub samples:** https://github.com/spring-projects/spring-boot/tree/main/spring-boot-samples

### Docker
- **Docker Docs:** https://docs.docker.com
- **Docker Compose docs:** https://docs.docker.com/compose/
- **Play with Docker:** https://labs.play-with-docker.com — Free browser-based Docker lab.

### AI Integration
- **OpenAI API reference (compatible format):** https://platform.openai.com/docs/api-reference/chat
- **LangChain4j docs:** https://docs.langchain4j.dev
- **Vultr Serverless Inference:** https://www.vultr.com/products/serverless-inference/
- **DigitalOcean GenAI:** https://docs.digitalocean.com/products/genai/

### System Design (for later weeks)
- **Grokking the System Design Interview:** https://www.educative.io/courses/grokking-the-system-design-interview
- **ByteByteGo:** https://www.bytebytego.com
- **Alex Xu System Design Interview:** Books (Volume 1 & 2)
