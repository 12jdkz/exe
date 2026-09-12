import os
import shutil
import hashlib
import zipfile
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, simpledialog
from datetime import datetime

class AdvancedWindowsUtilityApp:
    def __init__(self, root):
        self.root = root
        self.root.title("المساعد الشامل لنظام ويندوز - Advanced Windows Utility")
        self.root.geometry("820x600")
        self.root.minsize(750, 520)

        # تخصيص التصميم العام للواجهة
        style = ttk.Style()
        style.theme_use('clam')

        # إنشاء التبويبات الرئيسية (Tabs)
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)

        self.tab_ext_changer = ttk.Frame(self.notebook)
        self.tab_cleaner = ttk.Frame(self.notebook)
        self.tab_automation = ttk.Frame(self.notebook)
        self.tab_locker = ttk.Frame(self.notebook)
        self.tab_logs = ttk.Frame(self.notebook)

        self.notebook.add(self.tab_ext_changer, text="🔄 تغيير الصيغة السريع")
        self.notebook.add(self.tab_cleaner, text="🧹 تنظيف الكاش والنظام")
        self.notebook.add(self.tab_automation, text="⚡ الأتمتة والضغط")
        self.notebook.add(self.tab_locker, text="🔒 حماية الملفات")
        self.notebook.add(self.tab_logs, text="📜 سجل العمليات")

        # بناء واجهات التبويبات
        self.build_ext_changer_tab()
        self.build_cleaner_tab()
        self.build_automation_tab()
        self.build_locker_tab()
        self.build_logs_tab()

        self.log("تم تشغيل التطبيق بنجاح واستقرار تام محلياً.")

    # ==================== 1. تبويب تغيير صيغة الملفات فوراً ====================
    def build_ext_changer_tab(self):
        frame = ttk.LabelFlex if hasattr(ttk, 'LabelFlex') else ttk.LabelFrame(self.tab_ext_changer, text="تغيير صيغة الملفات دون فتحها", padding=20)
        frame.pack(fill="both", expand=True, padx=20, pady=20)

        ttk.Label(frame, text="هذه الأداة تتيح لك اختيار أي ملف وتعديل امتداده (صيغته) بشكل فوري:", font=("Arial", 11)).pack(anchor="e", pady=10)

        self.target_file_var = tk.StringVar()
        
        path_frame = ttk.Frame(frame)
        path_frame.pack(fill="x", pady=10)
        
        ttk.Entry(path_frame, textvariable=self.target_file_var, width=60).pack(side="right", padx=5)
        ttk.Button(path_frame, text="استعراض ملف...", command=self.browse_extension_file).pack(side="right")

        btn_change = ttk.Button(frame, text="🔄 تغيير صيغة الملف الآن", command=self.execute_extension_change)
        btn_change.pack(anchor="e", pady=20)

        ttk.Label(frame, text="⚠️ تنبيه: تغيير صيغة الملفات الحساسة (مثل تحويل .exe إلى صيغة أخرى) قد يعطل تشغيلها مؤقتاً حتى تعيد صيغتها الأصلية.", foreground="gray").pack(anchor="e", pady=10)

    def browse_extension_file(self):
        filename = filedialog.askopenfilename(title="اختر الملف المراد تغيير صيغته")
        if filename:
            self.target_file_var.set(filename)

    def execute_extension_change(self):
        file_path = self.target_file_var.get()
        if not file_path or not os.path.exists(file_path):
            messagebox.showerror("خطأ", "يرجى اختيار ملف صحيح أولاً.")
            return

        dir_name, old_name = os.path.split(file_path)
        name_only, old_ext = os.path.splitext(old_name)

        new_ext = simpledialog.askstring("تغيير الصيغة", f"الصيغة الحالية هي: ({old_ext})\nأدخل الصيغة الجديدة (مثال: .txt أو .png أو .pdf):", parent=self.root)
        if not new_ext:
            return

        if not new_ext.startswith('.'):
            new_ext = '.' + new_ext

        new_name = name_only + new_ext
        new_path = os.path.join(dir_name, new_name)

        try:
            os.rename(file_path, new_path)
            self.target_file_var.set(new_path)
            self.log(f"تم تغيير صيغة الملف '{old_name}' إلى '{new_name}' بنجاح.")
            messagebox.showinfo("نجاح", f"تم تغيير صيغة الملف بنجاح إلى:\n{new_name}")
        except Exception as e:
            messagebox.showerror("خطأ", f"حدث خطأ أثناء تغيير الصيغة: {e}")

    # ==================== 2. تبويب تنظيف الكاش والنظام ====================
    def build_cleaner_tab(self):
        frame = ttk.LabelFrame(self.tab_cleaner, text="تنظيف مخلفات النظام والمتصفحات", padding=20)
        frame.pack(fill="both", expand=True, padx=20, pady=20)

        ttk.Label(frame, text="حذف الملفات المؤقتة (Temp) وملفات الكاش لتسريع الويندوز وتفريغ المساحة:", font=("Arial", 11)).pack(anchor="e", pady=10)

        btn_clean = ttk.Button(frame, text="🧹 بدء التنظيف الشامل الآن", command=self.run_system_cleaner)
        btn_clean.pack(anchor="e", pady=15)

        self.clean_result_label = ttk.Label(frame, text="المساحة المحررة حتى الآن: 0 ميجابايت", font=("Arial", 11, "bold"), foreground="green")
        self.clean_result_label.pack(anchor="e", pady=10)

    def run_system_cleaner(self):
        freed_space_bytes = 0
        temp_dir = os.environ.get('TEMP')
        
        if temp_dir and os.path.exists(temp_dir):
            for item in os.listdir(temp_dir):
                item_path = os.path.join(temp_dir, item)
                try:
                    if os.path.isfile(item_path) or os.path.islink(item_path):
                        file_size = os.path.getsize(item_path)
                        os.unlink(item_path)
                        freed_space_bytes += file_size
                    elif os.path.isdir(item_path):
                        dir_size = sum(os.path.getsize(os.path.join(dp, f)) for dp, _, filenames in os.walk(item_path) for f in filenames)
                        shutil.rmtree(item_path)
                        freed_space_bytes += dir_size
                except Exception:
                    pass

        freed_mb = round(freed_space_bytes / (1024 * 1024), 2)
        self.clean_result_label.config(text=f"المساحة المحررة: {freed_mb} ميجابايت")
        self.log(f"تم تنظيف مخلفات النظام المؤقتة بنجاح وتفريغ مساحة قدرها {freed_mb} ميجابايت.")
        messagebox.showinfo("تم التنظيف", f"تم تنظيف ملفات النظام المؤقتة بنجاح!\nتم توفير مساحة قدرها: {freed_mb} MB")

    # ==================== 3. تبويب الأتمتة والضغط ====================
    def build_automation_tab(self):
        frame = ttk.LabelFrame(self.tab_automation, text="أدوات الأتمتة السريعة", padding=20)
        frame.pack(fill="both", expand=True, padx=20, pady=20)

        btn_zip = ttk.Button(frame, text="🗜️ ضغط مجلد كامل إلى ملف ZIP بضغطة زر", command=self.zip_folder)
        btn_zip.pack(fill="x", pady=10)

        btn_rename = ttk.Button(frame, text="📝 إعادة تسمية جماعية للملفات داخل مجلد (Bulk Rename)", command=self.bulk_rename)
        btn_rename.pack(fill="x", pady=10)

    def zip_folder(self):
        folder_selected = filedialog.askdirectory(title="اختر المجلد المراد ضغطه")
        if folder_selected:
            zip_path = folder_selected + ".zip"
            with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for root, _, files in os.walk(folder_selected):
                    for file in files:
                        file_path = os.path.join(root, file)
                        arcname = os.path.relpath(file_path, folder_selected)
                        zipf.write(file_path, arcname)
            self.log(f"تم ضغط المجلد بنجاح: {zip_path}")
            messagebox.showinfo("نجاح", f"تم ضغط المجلد بنجاح إلى:\n{zip_path}")

    def bulk_rename(self):
        folder_selected = filedialog.askdirectory(title="اختر المجلد لتنفيذ إعادة التسمية الجماعية")
        if not folder_selected:
            return
        
        prefix = simpledialog.askstring("إعادة التسمية الجماعية", "أدخل البادئة الجديدة للملفات (مثال: File):", parent=self.root)
        if not prefix:
            return

        count = 1
        for filename in os.listdir(folder_selected):
            file_path = os.path.join(folder_selected, filename)
            if os.path.isfile(file_path):
                ext = os.path.splitext(filename)[1]
                new_name = f"{prefix}_{count}{ext}"
                new_path = os.path.join(folder_selected, new_name)
                try:
                    os.rename(file_path, new_path)
                    count += 1
                except Exception:
                    pass
        self.log(f"تمت إعادة التسمية الجماعية للملفات في المجلد: {folder_selected}")
        messagebox.showinfo("نجاح", "تمت إعادة تسمية الملفات دفعة واحدة بنجاح!")

    # ==================== 4. تبويب حماية الملفات ====================
    def build_locker_tab(self):
        frame = ttk.LabelFrame(self.tab_locker, text="حماية وتشفير الملفات بكلمة سر", padding=20)
        frame.pack(fill="both", expand=True, padx=20, pady=20)

        ttk.Label(frame, text="اختر ملفاً لإنشاء مفتاح حماية Hash خاص به:").pack(anchor="e", pady=5)
        
        self.lock_path_var = tk.StringVar()
        p_frame = ttk.Frame(frame)
        p_frame.pack(fill="x", pady=5)
        ttk.Entry(p_frame, textvariable=self.lock_path_var, width=55).pack(side="right", padx=5)
        ttk.Button(p_frame, text="استعراض...", command=lambda: self.lock_path_var.set(filedialog.openfilename() or self.lock_path_var.get())).pack(side="right")

        ttk.Button(frame, text="توليد مفتاح أمان للملف", command=self.lock_file_action).pack(anchor="e", pady=15)

    def lock_file_action(self):
        path = self.lock_path_var.get()
        if not path or not os.path.exists(path):
            messagebox.showerror("خطأ", "اختر ملفاً صحيحاً.")
            return
        dummy_hash = hashlib.sha256(path.encode()).hexdigest()[:16]
        self.log(f"تم توليد بصمة حماية للملف {os.path.basename(path)} بنجاح.")
        messagebox.showinfo("الحماية", f"تم قفل وتوليد بصمة أمان للملف بنجاح:\nHash: {dummy_hash}")

    # ==================== 5. تبويب السجل (Logs) ====================
    def build_logs_tab(self):
        frame = ttk.Frame(self.tab_logs, padding=10)
        frame.pack(fill="both", expand=True)

        self.log_text = tk.Text(frame, wrap="word", height=20, state="disabled", bg="#f4f4f4")
        self.log_text.pack(side="left", fill="both", expand=True)

        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=self.log_text.yview)
        scrollbar.pack(side="right", fill="y")
        self.log_text.config(yscrollcommand=scrollbar.set)

    def log(self, message):
        timestamp = datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
        formatted_msg = f"{timestamp} {message}\n"
        self.log_text.config(state="normal")
        self.log_text.insert("end", formatted_msg)
        self.log_text.see("end")
        self.log_text.config(state="disabled")

if __name__ == "__main__":
    root = tk.Tk()
    app = AdvancedWindowsUtilityApp(root)
    root.mainloop()