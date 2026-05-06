# coding:utf-8
import hashlib
import base64
from Crypto.Cipher import DES,AES
from Crypto.Util.Padding import pad,unpad
import os
import io
import re
from PIL import Image, ImageSequence
class Common(object):

    def md5(self, pwd):
        md5 = hashlib.md5()
        md5.update(pwd.encode())
        return md5.hexdigest()


    def extract_text_from_docx_base64(b64_content):
        """
        从docx的base64内容中提取文本
        docx文件本质是zip包，包含word/document.xml
        """
        try:
            docx_bytes = base64.b64decode(b64_content)
            if len(docx_bytes) < 4:
                print(f"extract_text_from_docx_base64 error: File too small")
                return None
            if docx_bytes[0:2] != b'PK':
                print(f"extract_text_from_docx_base64 error: Not a valid zip file (docx). First bytes: {docx_bytes[0:4]}")
                return None
            docx_io = io.BytesIO(docx_bytes)
            import zipfile
            with zipfile.ZipFile(docx_io, 'r') as zf:
                if 'word/document.xml' not in zf.namelist():
                    print(f"extract_text_from_docx_base64 error: No word/document.xml in archive. Files: {zf.namelist()[:10]}")
                    return None
                xml_content = zf.read('word/document.xml').decode('utf-8')
                text = re.sub(r'<[^>]+>', '', xml_content)
                text = re.sub(r'\s+', ' ', text).strip()
                return text
        except Exception as e:
            print(f"extract_text_from_docx_base64 error: {e}")
        return None

    def compress_image_to_base64_preserve_color(file_path,
                                                   max_bytes=100 * 1024,
                                                   max_size=(512, 512),
                                                   min_dimension=200):
           """
           压缩图片并返回 (base64_str, content_type)
           要点：
           - 不会把带透明通道的 PNG 填白或转成 JPEG（保留颜色与 alpha）
           - 会等比缩放以降低体积；对 JPEG 还会降低 quality
           - 动画 GIF 不压缩（直接返回原始 bytes）
           """
           ext = os.path.splitext(file_path)[1].lower()
           content_type_map = {
               '.jpg': 'image/jpeg',
               '.jpeg': 'image/jpeg',
               '.png': 'image/png',
               '.gif': 'image/gif',
               '.bmp': 'image/bmp',
               '.webp': 'image/webp'
           }
           content_type = content_type_map.get(ext, 'application/octet-stream')

           with open(file_path, 'rb') as f:
               original_bytes = f.read()

           # 如果文件已小于阈值，直接返回原始
           if len(original_bytes) <= max_bytes:
               return base64.b64encode(original_bytes).decode('utf-8'), content_type

           # 尝试用 Pillow 处理
           try:
               img = Image.open(io.BytesIO(original_bytes))

               # 动画 GIF：不处理动画，直接返回原始 bytes（避免破坏动画）
               if getattr(img, "is_animated", False) and ext == '.gif':
                   return base64.b64encode(original_bytes).decode('utf-8'), 'image/gif'

               # 初次等比缩放到 max_size（如果需要）
               img.thumbnail(max_size, Image.LANCZOS)

               # 现在按不同格式采取策略
               buffer = io.BytesIO()

               if ext in ('.jpg', '.jpeg'):
                   # JPEG：逐步降低 quality，同时可进一步缩小尺寸
                   quality = 85
                   while True:
                       buffer.seek(0)
                       buffer.truncate(0)
                       save_kwargs = {'format': 'JPEG', 'quality': quality, 'optimize': True}
                       # 保证是 RGB
                       if img.mode != 'RGB':
                           tmp = img.convert('RGB')
                       else:
                           tmp = img
                       tmp.save(buffer, **save_kwargs)
                       data = buffer.getvalue()
                       if len(data) <= max_bytes or quality <= 30:
                           break
                       # 若质量下降到阈值还不够，则先进一步等比缩放再继续
                       quality = max(30, int(quality * 0.8))
                       # 若图片仍然较大，缩小 90%
                       w, h = img.size
                       if min(w, h) > min_dimension:
                           img = img.resize((max(min_dimension, int(w * 0.9)), max(min_dimension, int(h * 0.9))),
                                            Image.LANCZOS)
                       else:
                           # 达到最小尺寸，停止缩放—仅靠 quality 继续
                           continue

                   return base64.b64encode(data).decode('utf-8'), 'image/jpeg'

               elif ext == '.png':
                   # PNG：保留 alpha，不合成背景。使用 optimize + compress_level，并通过进一步缩放尝试减小体积
                   compress_level = 9  # 0-9，9 最大压缩（慢）
                   # 先尝试保存一次
                   buffer.seek(0)
                   buffer.truncate(0)
                   save_kwargs = {'format': 'PNG', 'optimize': True, 'compress_level': compress_level}
                   # 注意：不要转成 RGB 如果原图带 alpha（RGBA），保持原模式
                   img.save(buffer, **save_kwargs)
                   data = buffer.getvalue()

                   # 如果仍然过大，尝试逐步等比缩放（保持颜色与透明度）
                   while len(data) > max_bytes:
                       w, h = img.size
                       if min(w, h) <= min_dimension:
                           # 无法再缩小（达到最小尺寸），跳出
                           break
                       new_w = max(min_dimension, int(w * 0.9))
                       new_h = max(min_dimension, int(h * 0.9))
                       img = img.resize((new_w, new_h), Image.LANCZOS)
                       buffer.seek(0)
                       buffer.truncate(0)
                       img.save(buffer, **save_kwargs)
                       data = buffer.getvalue()

                   return base64.b64encode(data).decode('utf-8'), 'image/png'

               elif ext == '.webp':
                   # WebP：默认尽量保留无损（如果原为有损，保持近似），使用 lossless=True 会保留精确像素
                   # 这里优先无损以保证颜色不变
                   buffer.seek(0)
                   buffer.truncate(0)
                   try:
                       img.save(buffer, format='WEBP', lossless=True, method=6)
                       data = buffer.getvalue()
                   except Exception:
                       # 如果不支持 lossless，回退为常规保存
                       img.save(buffer, format='WEBP', quality=80, method=6)
                       data = buffer.getvalue()

                   # 若仍太大，尝试缩放
                   while len(data) > max_bytes:
                       w, h = img.size
                       if min(w, h) <= min_dimension:
                           break
                       img = img.resize((max(min_dimension, int(w * 0.9)), max(min_dimension, int(h * 0.9))),
                                        Image.LANCZOS)
                       buffer.seek(0)
                       buffer.truncate(0)
                       try:
                           img.save(buffer, format='WEBP', lossless=True, method=6)
                       except Exception:
                           img.save(buffer, format='WEBP', quality=80, method=6)
                       data = buffer.getvalue()

                   return base64.b64encode(data).decode('utf-8'), 'image/webp'

               else:
                   # 其它格式（bmp 等）：尝试以 PNG 或原格式保存但不改变色彩处理
                   buffer.seek(0)
                   buffer.truncate(0)
                   # 先尝试原格式保存（若 pillow 支持）
                   try:
                       img.save(buffer, format=img.format)
                       data = buffer.getvalue()
                   except Exception:
                       # 回退保存为 PNG（保留色彩与 alpha）
                       buffer.seek(0)
                       buffer.truncate(0)
                       img.save(buffer, format='PNG', optimize=True)
                       data = buffer.getvalue()

                   # 若太大则缩放
                   while len(data) > max_bytes:
                       w, h = img.size
                       if min(w, h) <= min_dimension:
                           break
                       img = img.resize((max(min_dimension, int(w * 0.9)), max(min_dimension, int(h * 0.9))),
                                        Image.LANCZOS)
                       buffer.seek(0)
                       buffer.truncate(0)
                       try:
                           img.save(buffer, format=img.format)
                       except Exception:
                           img.save(buffer, format='PNG', optimize=True)
                       data = buffer.getvalue()

                   # 根据保存方式设置 content_type（偏保守，若不明确则用 png）
                   return base64.b64encode(data).decode('utf-8'), content_type_map.get(ext, 'image/png')

           except Exception as e:
               # 出错回退到原始 bytes（保证不改变颜色）
               # print(f"compress error: {e}")
               return base64.b64encode(original_bytes).decode('utf-8'), content_type_map.get(ext,
                                                                                             'application/octet-stream')

    def append_images_to_content_preserve_color(self, fileNames, content,
                                                upload_dir=None,
                                                max_bytes=100 * 1024,
                                                max_size=(128, 128)):
        """
        处理逗号分隔的多个文件，根据扩展名判断类型：
        - 图片：压缩并转为base64图片
        - 文档(docx等)：提取文本内容追加到prompt
        """
        if not fileNames:
            return content

        if upload_dir is None:
            upload_dir = os.path.join(os.getcwd(), "templates", "upload")

        image_exts = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp'}
        doc_exts = {'.docx', '.doc', '.txt', '.pdf'}

        for fileName in fileNames.split(","):
            fileName = fileName.strip()
            if not fileName:
                continue

            filePath = os.path.join(upload_dir, fileName)
            if not os.path.exists(filePath):
                continue

            ext = os.path.splitext(fileName)[1].lower()
            print("ext:", ext)

            if ext in doc_exts:
                if ext == '.docx':
                    print("filePath:",filePath)
                    text = self.extract_text_from_docx_base64(
                        base64.b64encode(open(filePath, 'rb').read()).decode('utf-8')
                    )
                    if text:
                        print("text:",text)
                        content += f"\n\n[文档：{fileName}]\n{text}"
                elif ext == '.txt':
                    try:
                        with open(filePath, 'r', encoding='utf-8') as f:
                            text = f.read()
                        content += f"\n\n[文档：{fileName}]\n{text}"
                    except:
                        pass
            elif ext in image_exts:
                b64, ctype = self.compress_image_to_base64_preserve_color(
                    filePath, max_bytes=max_bytes, max_size=max_size
                )
                content += f"\n\n[图片：{fileName}]\n![image](data:{ctype};base64,{b64})"

        return content