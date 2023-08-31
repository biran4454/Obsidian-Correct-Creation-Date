import pywintypes, win32file, win32con
import os, time
import sys
def changeFileCreationTime(fname, newtime, editedtime):
    wintime = pywintypes.Time(newtime)
    editedtime = pywintypes.Time(editedtime)
    winfile = win32file.CreateFile(
        fname, win32con.GENERIC_WRITE,
        win32con.FILE_SHARE_READ | win32con.FILE_SHARE_WRITE | win32con.FILE_SHARE_DELETE,
        None, win32con.OPEN_EXISTING,
        win32con.FILE_ATTRIBUTE_NORMAL, None)

    win32file.SetFileTime(winfile, wintime, None, editedtime)


    winfile.close()

# usage:
# main.py [root_dir]
if __name__ == '__main__':
    if len(sys.argv) > 1:
        root_dir = sys.argv[1]
    else:
        root_dir = os.getcwd()
    for root, dirs, files in os.walk(root_dir):
        if root.split('\\')[-1].startswith('.') or root.split('\\')[-1].startswith('_'):
            continue
        for file in files:
            if file.endswith('.md'):
                # get created time from frontmatter
                created_time = ''
                edited_time = ''
                with open(os.path.join(root, file), 'r', encoding='utf-8') as f:
                    in_frontmatter = False
                    for line in f.readlines():
                        if line == '---\n':
                            if in_frontmatter:
                                break
                            in_frontmatter = not in_frontmatter
                            continue
                        if in_frontmatter and line.startswith('created'):
                            created_time = line.split('created: ')[1].strip()
                        if in_frontmatter and line.startswith('updated'):
                            edited_time = line.split('updated: ')[1].strip()
                # change file created time
                if created_time:
                    created_time = time.mktime(time.strptime(created_time, '%Y-%m-%d %H:%M:%SZ'))
                    if time.localtime(created_time).tm_isdst == 1:
                        created_time += 3600
                if edited_time:
                    edited_time = time.mktime(time.strptime(edited_time, '%Y-%m-%d %H:%M:%SZ'))
                    if time.localtime(edited_time).tm_isdst == 1:
                        edited_time += 3600
                changeFileCreationTime(os.path.join(root, file), created_time, edited_time)