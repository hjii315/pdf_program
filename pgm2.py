# GUI 프로그램을 만들기 위한 tkinter 라이브러리를 불러옵니다.
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

# 외부 프로그램을 실행하기 위한 subprocess 라이브러리를 불러옵니다.
import subprocess
# 파일 경로를 다루기 위한 os 라이브러리를 불러옵니다.
import os

# --- 설정 (사용자 환경에 맞게 수정!) ---
# 1단계에서 설치한 Ghostscript의 gswin64c.exe 파일 경로를 여기에 입력하세요.
# 경로의 역슬래시(\)는 두 번씩 (\\) 또는 슬래시(/)로 바꿔주어야 에러가 나지 않습니다.
GHOSTSCRIPT_PATH = "C:\\Program Files\\gs\\gs10.03.1\\bin\\gswin64c.exe"

# --- 전역 변수 ---
input_file_path = ""

# --- 함수 정의 ---
def check_ghostscript():
    """프로그램 시작 시 Ghostscript 경로가 올바른지 확인하는 함수"""
    if not os.path.exists(GHOSTSCRIPT_PATH):
        messagebox.showerror(
            "오류",
            f"Ghostscript를 찾을 수 없습니다!\n"
            f"GHOSTSCRIPT_PATH 변수의 경로를 확인해주세요.\n"
            f"현재 설정된 경로: {GHOSTSCRIPT_PATH}"
        )
        root.destroy() # 프로그램 종료

def select_file():
    """'파일 선택' 버튼을 눌렀을 때 실행될 함수"""
    global input_file_path
    path = filedialog.askopenfilename(
        title="압축할 PDF 파일을 선택하세요",
        filetypes=[("PDF files", "*.pdf")]
    )
    if path:
        input_file_path = path
        filename = os.path.basename(path)
        file_label.config(text=f"선택된 파일: {filename}")

def compress_pdf_with_ghostscript():
    """'압축 시작' 버튼을 눌렀을 때 실행될 함수"""
    if not input_file_path:
        messagebox.showerror("오류", "먼저 PDF 파일을 선택해주세요!")
        return

    # 1. 압축 품질 설정 가져오기
    quality = quality_var.get()

    # 2. 저장할 파일 경로 만들기
    base, ext = os.path.splitext(input_file_path)
    output_file_path = f"{base}_compressed_gs{ext}"

    # 3. Ghostscript 실행 명령어 만들기
    # -dPDFSETTINGS 옵션이 압축 품질을 결정합니다.
    command = [
        GHOSTSCRIPT_PATH,
        "-sDEVICE=pdfwrite",
        "-dCompatibilityLevel=1.4",
        f"-dPDFSETTINGS=/{quality}",
        "-dNOPAUSE",
        "-dQUIET",
        "-dBATCH",
        f"-sOutputFile={output_file_path}",
        input_file_path
    ]

    try:
        # 4. 터미널(cmd)에서 명령어를 실행하듯이 Ghostscript를 실행합니다.
        status_label.config(text="압축 중입니다... 잠시만 기다려주세요.")
        root.update_idletasks() # 라벨 텍스트 변경을 바로 화면에 반영

        subprocess.run(command, check=True)
        
        messagebox.showinfo("완료", f"PDF 압축이 완료되었습니다!\n저장 위치: {output_file_path}")

    except FileNotFoundError:
        messagebox.showerror("오류", "Ghostscript를 찾을 수 없습니다. GHOSTSCRIPT_PATH를 확인해주세요.")
    except subprocess.CalledProcessError as e:
        messagebox.showerror("오류", f"압축 중 오류가 발생했습니다: {e}")
    finally:
        # 완료 또는 에러 발생 후 상태 메시지 초기화
        status_label.config(text="")


# --- GUI 화면 구성 ---
root = tk.Tk()
root.title("Ghostscript PDF 압축기")
root.geometry("500x280")
root.resizable(False, False)

# 제목 라벨
title_label = tk.Label(root, text="Ghostscript PDF 압축 프로그램", font=("Helvetica", 16, "bold"))
title_label.pack(pady=15)

# 파일 선택 버튼
select_button = tk.Button(root, text="PDF 파일 선택", width=25, command=select_file)
select_button.pack(pady=5)

# 선택된 파일 이름 라벨
file_label = tk.Label(root, text="아직 파일이 선택되지 않았습니다.", fg="gray")
file_label.pack(pady=5)

# 압축 품질 선택 드롭다운 메뉴
quality_frame = tk.Frame(root)
quality_frame.pack(pady=10)

quality_label = tk.Label(quality_frame, text="압축 품질 선택:")
quality_label.pack(side=tk.LEFT, padx=5)

quality_options = ["screen", "ebook", "printer", "prepress"]
quality_var = tk.StringVar(value="ebook") # 기본값은 'ebook'으로 설정
quality_menu = ttk.Combobox(quality_frame, textvariable=quality_var, values=quality_options, state="readonly", width=15)
quality_menu.pack(side=tk.LEFT)

# 압축 시작 버튼
compress_button = tk.Button(root, text="압축 시작!", width=25, height=2, bg="lightgreen", command=compress_pdf_with_ghostscript)
compress_button.pack(pady=10)

# 상태 메시지 라벨
status_label = tk.Label(root, text="", fg="blue")
status_label.pack(pady=5)

# 프로그램 시작 시 Ghostscript 경로 확인
root.after(100, check_ghostscript)

# GUI 프로그램 실행
root.mainloop()