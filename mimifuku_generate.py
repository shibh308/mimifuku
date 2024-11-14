from speech import generate_and_save_audio
from scrapbox import get_page_content, get_page_list
import hashlib
import typing
import pathlib

OUTPUT_ROOT_DIR = pathlib.Path(__file__).parent / 'output'
PAPERS_DIR = OUTPUT_ROOT_DIR / 'papers'
CTF_DIR = OUTPUT_ROOT_DIR / 'ctf'
HASH_FILE = OUTPUT_ROOT_DIR / 'hash.txt'

def mp3_name(dir: pathlib.Path, title: str) -> pathlib.Path:
    return dir / f'{title}.mp3'

def line_fn(line):
    if line == '':
        return line
    return line.strip() + '。\n'

def title_and_lines_to_text(title: str, lines: str, prefix=None) -> str:
    title_line = f'{prefix}、{title}' if prefix is not None else title
    content = [title_line] + lines
    return ''.join(map(line_fn, content)).strip()

def generate_and_save_audio_with_hash_check(text: str, out_path: pathlib.Path, hash_dict: typing.Dict[str, str]):
    relative_path = out_path.relative_to(OUTPUT_ROOT_DIR)
    relative_path_hash = hashlib.md5(str(relative_path).encode()).hexdigest()
    text_hash = hashlib.md5(text.encode()).hexdigest()
    if relative_path_hash in hash_dict and hash_dict[relative_path_hash] == text_hash:
        print(f"skip: {out_path}")
    else:
        hash_dict[relative_path_hash] = text_hash
        generate_and_save_audio(text, out_path)

def gen_all_papers(hash_dict: typing.Dict[str, str]):
    # 論文まとめ
    pages = get_page_list("checkedpapers")
    for title in pages:
        if title == 'Template':
            continue
        out_path = mp3_name(PAPERS_DIR, title)
        lines = get_page_content("checkedpapers", title)
        if '概要' in lines:
            text = title_and_lines_to_text(title, lines[lines.index('概要') + 1:], '論文タイトル')
            generate_and_save_audio_with_hash_check(text, out_path, hash_dict)

def fetch_and_generate_and_save(project: str, title: str, out_dir: pathlib.Path, hash_dict: typing.Dict[str, str], prefix=None):
    out_path = mp3_name(out_dir, title)
    lines = get_page_content(project, title)
    text = title_and_lines_to_text(title, lines, prefix=prefix)
    generate_and_save_audio_with_hash_check(text, out_path, hash_dict)

def read_hash_dict() -> typing.Dict[str, str]:
    if not HASH_FILE.exists():
        return dict()
    with open(HASH_FILE, 'r') as f:
        hash_list = f.readlines()
        hash_dict = dict(map(lambda x: x.strip().split(':'), hash_list))
        return hash_dict

def write_hash_dict(hash_dict: typing.Dict[str, str]):
    with open(HASH_FILE, 'w') as f:
        hash_list = '\n'.join(map(lambda x: f'{x[0]}:{x[1]}', hash_dict.items()))
        f.writelines(hash_list)

def main():
    hash_dict = read_hash_dict()
    gen_all_papers(hash_dict)
    fetch_and_generate_and_save('checkedpapers', '研究アイデア集', OUTPUT_ROOT_DIR, hash_dict)
    # fetch_and_generate_and_save('solvedproblems', 'Web典型', CTF_DIR, old_hash_list, new_hash_list)
    # fetch_and_generate_and_save('solvedproblems', 'Crypto典型', CTF_DIR, old_hash_list, new_hash_list)
    # fetch_and_generate_and_save('solvedproblems', 'Pwn典型', CTF_DIR, old_hash_list, new_hash_list)
    write_hash_dict(hash_dict)


if __name__ == '__main__':
    main()
