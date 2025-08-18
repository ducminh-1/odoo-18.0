import os
import re
import shutil

MODULE_PATH = "/home/minhle/odoo-18.0/custom_addons/mhd_data_old/views"

def process_file(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    new_content = content
    changed = False

    # 1. Đổi <tree ...> thành <list ...>
    # Bắt đầu bằng <tree, không phải <tree_ hay <treeX
    new_content, n1 = re.subn(
        r"<\s*tree(\s[^>]*)?>",
        lambda m: "<list{}>".format(m.group(1) if m.group(1) else ""),
        new_content
    )

    # 2. Đổi </tree> thành </list>
    new_content, n2 = re.subn(
        r"</\s*tree\s*>",
        "</list>",
        new_content
    )

    # 3. Trong view_mode đổi "tree" → "list"
    # Chỉ thay bên trong field name="view_mode"
    new_content, n3 = re.subn(
        r'(<field\s+name\s*=\s*"view_mode"\s*>)([^<]+)(</field>)',
        lambda m: m.group(1) + m.group(2).replace("tree", "list") + m.group(3),
        new_content
    )

    if n1 > 0 or n2 > 0 or n3 > 0:
        changed = True

    if changed:
        shutil.copy(file_path, file_path + ".bak")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(new_content)
        print(f"✅ Updated {file_path} ({n1} mở, {n2} đóng, {n3} view_mode)")

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
    print("🎯 Hoàn tất cập nhật tree → list + view_mode.")
