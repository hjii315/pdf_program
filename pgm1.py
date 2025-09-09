# GUI 프로그램을 만들기 위한 tkinter 라이브러리를 불러옵니다.
import tkinter as tk
from tkinter import filedialog  # 파일 선택 대화상자를 위한 모듈
from tkinter import messagebox  # 메시지 박스를 위한 모듈

# PDF 파일을 다루기 위한 PyMuPDF 라이브러리(fitz)를 불러옵니다.
import fitz
# 파일 경로를 다루기 위한 os 라이브러리를 불러옵니다.
import os

# 전역 변수로 선택된 파일 경로를 저장할 변수를 만듭니다.
file_path = ""

# --- 함수 정의 ---

def select_file():
    """'파일 선택' 버튼을 눌렀을 때 실행될 함수"""
    global file_path
    # PDF 파일만 선택할 수 있도록 파일 형식을 지정합니다.
    # askopenfilename은 파일 선택 대화상자를 열고, 선택된 파일의 전체 경로를 반환합니다.
    path = filedialog.askopenfilename(
        title="압축할 PDF 파일을 선택하세요",
        filetypes=[("PDF files", "*.pdf")]
    )
    
    # 사용자가 파일을 선택했다면
    if path:
        file_path = path
        # 파일 경로에서 파일 이름만 추출합니다.
        filename = os.path.basename(path)
        # 선택된 파일 이름을 화면의 라벨에 표시합니다.
        file_label.config(text=f"선택된 파일: {filename}")
        print(f"선택된 파일: {file_path}") # 터미널에도 확인용으로 출력

def compress_pdf():
    """'압축 시작' 버튼을 눌렀을 때 실행될 함수"""
    global file_path
    
    # 파일이 선택되지 않았다면, 에러 메시지를 보여주고 함수를 종료합니다.
    if not file_path:
        messagebox.showerror("오류", "먼저 PDF 파일을 선택해주세요!")
        return
        
    try:
        # 1. 원본 PDF 파일 열기
        doc = fitz.open(file_path)
        
        # 2. 저장할 파일 경로 만들기
        # 원본 파일 경로에서 파일 이름과 확장자를 분리합니다.
        base, ext = os.path.splitext(file_path)
        # 새 파일 이름 (예: report.pdf -> report_compressed.pdf)
        output_path = f"{base}_compressed{ext}"

        # 3. 압축 옵션을 적용하여 파일 저장하기
        # garbage=4: 사용하지 않는 데이터를 정리하여 용량을 줄입니다. (가장 강력한 정리 옵션)
        # deflate=True: 파일 내부의 데이터 스트림을 압축합니다.
        doc.save(output_path, garbage=4, deflate=True)
        doc.close()
        
        # 4. 완료 메시지 보여주기
        messagebox.showinfo("완료", f"PDF 압축이 완료되었습니다!\n저장 위치: {output_path}")

    except Exception as e:
        # 압축 중 에러가 발생하면 에러 메시지를 보여줍니다.
        messagebox.showerror("오류", f"압축 중 오류가 발생했습니다:\n{e}")

# --- GUI 화면 구성 ---

# 1. 메인 윈도우 생성
root = tk.Tk()
root.title("초간단 PDF 압축기")
root.geometry("450x200") # 창 크기 설정
root.resizable(False, False) # 창 크기 변경 불가

# 2. 제목 라벨 생성
title_label = tk.Label(root, text="PDF 압축 프로그램", font=("Helvetica", 16, "bold"))
title_label.pack(pady=10) # pack()은 위젯을 창에 배치, pady는 위아래 여백

# 3. 파일 선택 버튼 생성
select_button = tk.Button(root, text="PDF 파일 선택", width=20, command=select_file)
select_button.pack(pady=10)

# 4. 선택된 파일 이름을 보여줄 라벨 생성
file_label = tk.Label(root, text="아직 파일이 선택되지 않았습니다.", fg="gray")
file_label.pack(pady=5)

# 5. 압축 시작 버튼 생성
compress_button = tk.Button(root, text="압축 시작!", width=20, height=2, bg="lightblue", command=compress_pdf)
compress_button.pack(pady=10)

# 6. GUI 프로그램 실행
root.mainloop()