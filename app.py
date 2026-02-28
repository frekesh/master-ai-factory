import gradio as gr
import urllib.parse
import random
import requests
import os

style_prompts = {
    "بدون ستايل (حسب الوصف)": "",
    "أنيميشن سينمائي": "3D animation, Pixar style, highly detailed, vibrant colors, unreal engine 5 render, cinematic lighting",
    "ثقافة مغربية": "Moroccan authentic aesthetic, traditional architecture, warm colors, medina lighting, highly detailed",
    "سايبر بانك": "cyberpunk style, neon lights, futuristic city, highly detailed, 8k",
    "واقعي جداً": "photorealistic, 8k, raw photo, ultra-detailed, photography"
}

def generate_professional_prompt(idea):
    if not idea.strip(): return "⚠️ المرجو كتابة فكرتك أولاً!"
    system_instruction = "Write a highly detailed, descriptive text-to-image prompt based on this idea. Return ONLY the English prompt."
    full_req = f"{system_instruction} Idea: {idea}"
    encoded_req = urllib.parse.quote(full_req)
    
    try:
        response = requests.get(f"https://text.pollinations.ai/{encoded_req}", timeout=20)
        if response.status_code == 200: return response.text
        return "❌ خطأ في التوليد."
    except:
        return "❌ فشل الاتصال."

def generate_image_vip(prompt, style_name):
    if not prompt.strip(): return None, "⚠️ الوصف فارغ!"
    full_prompt = f"{prompt}, {style_prompts[style_name]}"
    encoded_prompt = urllib.parse.quote(full_prompt)
    seed = random.randint(1, 1000000)
    url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1280&height=720&nologo=true&seed={seed}"
    
    try:
        response = requests.get(url, timeout=30)
        if response.status_code == 200:
            file_path = f"img_{seed}.jpg"
            with open(file_path, "wb") as f:
                f.write(response.content)
            return file_path, "✅ تم التوليد بنجاح!"
        return None, "❌ خطأ من السيرفر."
    except:
        return None, "❌ فشل الاتصال."

with gr.Blocks(theme=gr.themes.Soft(primary_hue="indigo")) as demo:
    gr.Markdown("<h1 style='text-align: center;'>👑 مصنع الماستر الدائم 👑</h1>")
    
    with gr.Tabs():
        with gr.TabItem("💡 صانع البرومبت"):
            idea_input = gr.Textbox(label="فكرتك (بالدارجة أو العربية)", lines=2)
            btn_prompt = gr.Button("توليد الوصف الإنجليزي 🪄", variant="primary")
            prompt_output = gr.Textbox(label="البرومبت الجاهز", lines=3)
            btn_prompt.click(fn=generate_professional_prompt, inputs=idea_input, outputs=prompt_output)

        with gr.TabItem("🖼️ مصنع الصور"):
            with gr.Row():
                with gr.Column(scale=2):
                    img_prompt_in = gr.Textbox(label="البرومبت (بالإنكليزية)", lines=3)
                    img_style = gr.Dropdown(choices=list(style_prompts.keys()), value="بدون ستايل (حسب الوصف)", label="🎨 الستايل الفني")
                    btn_image = gr.Button("توليد الصورة 🚀", variant="primary")
                with gr.Column(scale=3):
                    img_out = gr.Image(label="الصورة النهائية", type="filepath")
                    img_status = gr.Textbox(label="الحالة")
            btn_image.click(fn=generate_image_vip, inputs=[img_prompt_in, img_style], outputs=[img_out, img_status])

# هذا السطر هو السر لكي يعمل التطبيق على سيرفرات استضافة الويب الحقيقية
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 7860))
    demo.launch(server_name="0.0.0.0", server_port=port)