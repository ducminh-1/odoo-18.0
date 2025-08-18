import os
import re
import shutil
import ast

# Đường dẫn thư mục hoặc file
MODULE_PATH = "/home/minhle/odoo-18.0/custom_addons/mhd_valuation/views/real_estate_draft.xml"

# Regex tìm attrs có invisible hoặc required
pattern_attrs = re.compile(r'attrs\s*=\s*"({[^"]+})"')

def parse_condition_list(cond_list):
    """
    Chuyển list [('field', '=', val), '|', ('f2', '!=', val2)] 
    → biểu thức string 'field == val and f2 != val2'
    """
    expr_parts = []
    logic_stack = []

    for item in cond_list:
        if item == '|':
            logic_stack.append('or')
        elif item == '&':
            logic_stack.append('and')
        elif isinstance(item, (list, tuple)) and len(item) == 3:
            field, op, val = item
            op = '==' if op == '=' else op
            val_str = f"'{val}'" if isinstance(val, str) else str(val)
            expr_parts.append(f"{field} {op} {val_str}")
        else:
            expr_parts.append(str(item))

    # Nếu có nhiều logic_stack, gộp điều kiện
    if logic_stack:
        final_expr = []
        # Duyệt kết hợp theo thứ tự Odoo xử lý
        parts_iter = iter(expr_parts)
        first = next(parts_iter)
        final_expr.append(first)
        for op, part in zip(logic_stack, parts_iter):
            final_expr.append(op)
            final_expr.append(part)
        return " ".join(final_expr)
    else:
        return " and ".join(expr_parts)

def convert_attrs(attrs_str):
    """
    Chuyển attrs="{'invisible': [...], 'required': [...]}" sang invisible="..." required="..."
    """
    try:
        attrs_dict = ast.literal_eval(attrs_str)
    except Exception as e:
        print(f"⚠ Lỗi parse attrs: {e}")
        return attrs_str

    new_parts = []
    for key in ['invisible', 'required']:
        if key in attrs_dict:
            cond_list = attrs_dict[key]
            expr = parse_condition_list(cond_list)
            new_parts.append(f'{key}="{expr}"')

    return " ".join(new_parts)

def process_file(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    new_content = content
    matches = pattern_attrs.findall(content)

    for match in matches:
        new_attrs = convert_attrs(match)
        new_content = new_content.replace(f'attrs="{match}"', new_attrs)

    if new_content != content:
        shutil.copy(file_path, file_path + ".bak")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(new_content)
        print(f"✅ Updated: {file_path}")

def scan_folder(path):
    if os.path.isfile(path):
        process_file(path)
    else:
        for root, _, files in os.walk(path):
            for file in files:
                if file.endswith(".xml"):
                    process_file(os.path.join(root, file))

if __name__ == "__main__":
    scan_folder(MODULE_PATH)
    print("🎯 Hoàn tất cập nhật XML.")
