# поиск левого тега
p_tag = """<p>proga <span style=" color:#aa0000;">test text 123 proga example for the text</span> text</p>"""
start = p_tag.find("123")
end = start + 3
left_start = None
left_end = None
for i in range(start - 1, 0, -1):
    if p_tag[i] == ">" and not left_end:
        left_end = i + 1
    if p_tag[i] == "<" and not left_start:
        left_start = i

print(left_start, left_end)
print(p_tag[left_start:left_end])
