

```python
import unified_diff

before = 'one\ntwo\nthree\n'
after = 'three\ntwo\none\n'

diff = unified_diff.unified_diff(before, after)
print(diff)
'''
--- 
+++ 
@@ -1,3 +1,3 @@
+three
+two
 one
-two
-three
'''
assert unified_diff.apply(before, diff) == after
assert unified_diff.restore(after, diff) == before
```