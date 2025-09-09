import tkinter as tk
from tkinter import filedialog, messagebox
import subprocess
import os

# --- 설정 (사용자 환경에 맞게 수정!) ---
GHOSTSCRIPT_PATH = "C:\\Program Files\\gs\\gs10.05.1\\bin\\gswin64c.exe"

# --- 전역 변수 ---
input_file_path = ""

# --- 함수 정의 ---

def format_bytes(size):
    """파일 크기(바이트)를 KB, MB, GB 단위로 변환하는 함수"""
    if size == 0:
        return "0 B"
    power = 1024
    n = 0
    power_labels = {0: '', 1: 'K', 2: 'M', 3: 'G', 4: 'T'}
    while size >= power and n < len(power_labels):
        size /= power
        n += 1
    return f"{size:.2f} {power_labels[n]}B"

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
    dpi_value_label.config(text=f"{int(float(value))} DPI")

def compress_pdf_with_ghostscript():
    if not input_file_path:
        messagebox.showerror("오류", "먼저 PDF 파일을 선택해주세요!")
        return

    try:
        # **[추가]** 압축 전 원본 파일 크기 가져오기
        original_size = os.path.getsize(input_file_path)

        dpi = dpi_var.get()
        base, ext = os.path.splitext(input_file_path)
        output_file_path = f"{base}_compressed_{dpi}dpi{ext}"

        command = [
            GHOSTSCRIPT_PATH, "-sDEVICE=pdfwrite", "-dCompatibilityLevel=1.4",
            "-dDownsampleColorImages=true", "-dDownsampleGrayImages=true", "-dDownsampleMonoImages=true",
            f"-dColorImageResolution={dpi}", f"-dGrayImageResolution={dpi}", f"-dMonoImageResolution={dpi}",
            "-dNOPAUSE", "-dQUIET", "-dBATCH", f"-sOutputFile={output_file_path}",
            input_file_path
        ]

        status_label.config(text="압축 중입니다... 잠시만 기다려주세요.")
        root.update_idletasks()

        subprocess.run(command, check=True)
        
        # **[핵심 변경]** 압축 후 파일 크기를 가져와서 압축률 계산 및 메시지 생성
        compressed_size = os.path.getsize(output_file_path)
        
        # 보기 좋게 파일 크기 포맷 변경
        original_size_str = format_bytes(original_size)
        compressed_size_str = format_bytes(compressed_size)

        # 압축률 계산 (용량이 얼마나 감소했는지 %)
        if original_size > 0:
            saved_percentage = (1 - (compressed_size / original_size)) * 100
        else:
            saved_percentage = 0
        
        # 최종 결과 메시지 만들기
        result_message = (
            f"PDF 압축이 완료되었습니다!\n"
            f"저장 위치: {output_file_path}\n\n"
            f"원본 용량: {original_size_str}\n"
            f"압축 후 용량: {compressed_size_str}\n"
            f"✅ 용량 감소율: {saved_percentage:.2f}%"
        )
        messagebox.showinfo("완료", result_message)

    except FileNotFoundError:
        messagebox.showerror("오류", "Ghostscript를 찾을 수 없습니다. GHOSTSCRIPT_PATH를 확인해주세요.")
    except subprocess.CalledProcessError as e:
        messagebox.showerror("오류", f"압축 중 오류가 발생했습니다: {e}")
    except Exception as e:
        messagebox.showerror("오류", f"알 수 없는 오류가 발생했습니다: {e}")
    finally:
        status_label.config(text="")


# --- GUI 화면 구성 (이하 동일) ---
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

dpi_frame = tk.Frame(root)
dpi_frame.pack(pady=10)

dpi_label = tk.Label(dpi_frame, text="이미지 해상도(DPI) 조절:")
dpi_label.pack()

dpi_var = tk.IntVar(value=150)

dpi_slider = tk.Scale(
    dpi_frame, variable=dpi_var, from_=50, to=300,
    orient="horizontal", length=250, tickinterval=50,
    command=update_dpi_label
)
dpi_slider.pack()

dpi_value_label = tk.Label(dpi_frame, text="150 DPI", font=("Helvetica", 10, "bold"), fg="blue")
dpi_value_label.pack()

compress_button = tk.Button(root, text="압축 시작!", width=25, height=2, bg="lightgreen", command=compress_pdf_with_ghostscript)
compress_button.pack(pady=10)

status_label = tk.Label(root, text="", fg="blue")
status_label.pack(pady=5)

root.after(100, check_ghostscript)
root.mainloop()