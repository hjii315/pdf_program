import tkinter as tk
from tkinter import filedialog, messagebox
import subprocess
import os

# --- 설정 (사용자 환경에 맞게 수정!) ---
GHOSTSCRIPT_PATH = "C:\\Program Files\\gs\\gs10.05.1\\bin\\gswin64c.exe"

# --- 전역 변수 ---
input_file_path = ""

# --- 함수 정의 ---
def check_ghostscript():
    if not os.path.exists(GHOSTSCRIPT_PATH):
        messagebox.showerror(
            "오류",
            f"Ghostscript를 찾을 수 없습니다!\n"
            f"GHOSTSCRIPT_PATH 변수의 경로를 확인해주세요.\n"
            f"현재 설정된 경로: {GHOSTSCRIPT_PATH}"
        )
        root.destroy()

def select_file():
    global input_file_path
    path = filedialog.askopenfilename(
        title="압축할 PDF 파일을 선택하세요",
        filetypes=[("PDF files", "*.pdf")]
    )
    if path:
        input_file_path = path
        filename = os.path.basename(path)
        file_label.config(text=f"선택된 파일: {filename}")

def update_dpi_label(value):
    """슬라이더 값에 따라 DPI 라벨 텍스트를 업데이트하는 함수"""
    dpi_value_label.config(text=f"{int(float(value))} DPI")

def compress_pdf_with_ghostscript():
    if not input_file_path:
        messagebox.showerror("오류", "먼저 PDF 파일을 선택해주세요!")
        return

    # 1. 슬라이더에서 DPI 값 가져오기
    dpi = dpi_var.get()

    # 2. 저장할 파일 경로 만들기
    base, ext = os.path.splitext(input_file_path)
    output_file_path = f"{base}_compressed_{dpi}dpi{ext}"

    # 3. Ghostscript 실행 명령어 만들기 (핵심 변경 부분!)
    # -dPDFSETTINGS 대신 DPI를 직접 제어하는 옵션을 사용합니다.
    command = [
        GHOSTSCRIPT_PATH,
        "-sDEVICE=pdfwrite",
        "-dCompatibilityLevel=1.4",
        "-dDownsampleColorImages=true",   # 컬러 이미지 해상도 낮추기 활성화
        "-dDownsampleGrayImages=true",    # 흑백 이미지 해상도 낮추기 활성화
        "-dDownsampleMonoImages=true",    # 단색 이미지 해상도 낮추기 활성화
        f"-dColorImageResolution={dpi}", # 최종 컬러 이미지 해상도 설정
        f"-dGrayImageResolution={dpi}",  # 최종 흑백 이미지 해상도 설정
        f"-dMonoImageResolution={dpi}",  # 최종 단색 이미지 해상도 설정
        "-dNOPAUSE",
        "-dQUIET",
        "-dBATCH",
        f"-sOutputFile={output_file_path}",
        input_file_path
    ]

    try:
        status_label.config(text="압축 중입니다... 잠시만 기다려주세요.")
        root.update_idletasks()

        subprocess.run(command, check=True)
        
        messagebox.showinfo("완료", f"PDF 압축이 완료되었습니다!\n저장 위치: {output_file_path}")

    except FileNotFoundError:
        messagebox.showerror("오류", "Ghostscript를 찾을 수 없습니다. GHOSTSCRIPT_PATH를 확인해주세요.")
    except subprocess.CalledProcessError as e:
        messagebox.showerror("오류", f"압축 중 오류가 발생했습니다: {e}")
    finally:
        status_label.config(text="")


# --- GUI 화면 구성 ---
root = tk.Tk()
root.title("Ghostscript PDF 압축기 (DPI 조절)")
root.geometry("500x300")
root.resizable(False, False)

title_label = tk.Label(root, text="Ghostscript PDF 압축 프로그램", font=("Helvetica", 16, "bold"))
title_label.pack(pady=15)

select_button = tk.Button(root, text="PDF 파일 선택", width=25, command=select_file)
select_button.pack(pady=5)

file_label = tk.Label(root, text="아직 파일이 선택되지 않았습니다.", fg="gray")
file_label.pack(pady=5)

# --- 이미지 해상도(DPI) 조절 슬라이더 (핵심 변경 부분!) ---
dpi_frame = tk.Frame(root)
dpi_frame.pack(pady=10)

dpi_label = tk.Label(dpi_frame, text="이미지 해상도(DPI) 조절:")
dpi_label.pack()

# 슬라이더의 값을 저장할 변수
dpi_var = tk.IntVar(value=150)

# 슬라이더 위젯 생성
dpi_slider = tk.Scale(
    dpi_frame,
    variable=dpi_var,
    from_=50,           # 최소값
    to=300,             # 최대값
    orient="horizontal",# 수평 방향
    length=250,         # 슬라이더 길이
    tickinterval=50,    # 눈금 간격
    command=update_dpi_label # 값이 바뀔 때마다 update_dpi_label 함수 호출
)
dpi_slider.pack()

# 현재 선택된 DPI 값을 보여줄 라벨
dpi_value_label = tk.Label(dpi_frame, text="150 DPI", font=("Helvetica", 10, "bold"), fg="blue")
dpi_value_label.pack()

compress_button = tk.Button(root, text="압축 시작!", width=25, height=2, bg="lightgreen", command=compress_pdf_with_ghostscript)
compress_button.pack(pady=10)

status_label = tk.Label(root, text="", fg="blue")
status_label.pack(pady=5)

root.after(100, check_ghostscript)
root.mainloop()