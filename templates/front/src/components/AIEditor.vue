<template>
	<div>
		<!-- 图片上传组件辅助-->
		<el-upload :class="refname + 'upload'" :action="getActionUrl" name="file" :headers="header" :show-file-list="false" style="display: none;"
			:on-success="uploadSuccess" :on-error="uploadError" :before-upload="beforeUpload"></el-upload>

		<quill-editor class="editor" v-model="value" :ref="myQuillEditor" :options="editorOption"
			@blur="onEditorBlur($event)" @focus="onEditorFocus($event)" @change="onEditorChange($event)"></quill-editor>
	</div>
</template>
<script>
	// 工具栏配置
	const toolbarOptions = [
		["bold", "italic", "underline", "strike"], // 加粗 斜体 下划线 删除线
		["blockquote", "code-block"], // 引用  代码块
		[{
			header: 1
		}, {
			header: 2
		}], // 1、2 级标题
		[{
			list: "ordered"
		}, {
			list: "bullet"
		}], // 有序、无序列表
		[{
			script: "sub"
		}, {
			script: "super"
		}], // 上标/下标
		[{
			indent: "-1"
		}, {
			indent: "+1"
		}], // 缩进
		[{
			size: ["small", false, "large", "huge"]
		}], // 字体大小
		[{
			header: [1, 2, 3, 4, 5, 6, false]
		}], // 标题
		[{
			color: []
		}, {
			background: []
		}], // 字体颜色、字体背景颜色
		[{
			font: []
		}], // 字体种类
		[{
			align: []
		}], // 对齐方式
		["clean"], // 清除文本格式
		["link", "image", "video", "audio", "AI"], // 链接、图片、视频
	];
	var _EditorOption_ = function(page_this) {
		return {
			modules: {
				toolbar: {
					container: toolbarOptions,
					handlers: {
						image(value) {
							if (value) {
								console.log(document.querySelector("." + page_this.refname + "upload input"))
								// 触发input框选择图片文件
								document.querySelector("." + page_this.refname + "upload input").click();
							} else {
								this.quill.format("image", false);
							}
						},
						audio(value) {
							page_this.audioPlay()
						},
						AI(value) {
							page_this.changeDownList()
						}
					},
				},
			},
			placeholder: "请输入正文",
			initButton: function () {
				//在使用的页面中初始化按钮样式
				const audio= document.querySelector(".ql-audio");
				audio.title = '语言朗读'
				audio.style.cssText =
					"width:28px;height: 24px;color: #000";
				audio.className = "icon iconfont icon-gonggao18";
				
				
				const continuation= document.querySelector(".ql-AI");
				continuation.innerHTML = 'AI <span class="iconfont icon-jiantou35" style="padding: 0 0 0 5px">'
				continuation.style.cssText =
					"width: auto;height: 24px;color: #000;display: flex;align-items: center;background: #000;color:#fff;position: relative;cursor: pointer;border-radius: 5px;padding: 0 8px";
			},
		};
	};
	import config from "@/config/config";
	import {
		quillEditor
	} from "vue-quill-editor";
	import "quill/dist/quill.core.css";
	import "quill/dist/quill.snow.css";
	import "quill/dist/quill.bubble.css";

	export default {
		props: {
			/*编辑器的内容*/
			value: {
				type: String
			},
			action: {
				type: String
			},
			/*图片大小*/
			maxSize: {
				type: Number,
				default: 4000 //kb
			},
			myQuillEditor: {
				type: String
			}
		},

		components: {
			quillEditor
		},

		data() {
			return {
				baseUrl: config.baseUrl,
				baseUrl2: config.name,
				refname: this.myQuillEditor,
				content: this.value,
				quillUpdateImg: false, // 根据图片上传状态来确定是否显示loading动画，刚开始是false,不显示
				editorOption: _EditorOption_(this),
				header: {
					'Token': localStorage.getItem('frontToken')
				} // 有的图片服务器要求请求头需要有token
			};
		},
		computed: {
			// 计算属性的 getter
			getActionUrl: function() {
				return this.baseUrl2 + '/' + this.action;
			}
		},
		mounted() {
		    this.editorOption.initButton();
		},
		methods: {
			changeDownList() {
				let that = this
				
				var div
				if(document.getElementById('AIopera')) {
					div = document.getElementById('AIopera')
					if(div.innerHTML) {
						div.innerHTML = ''
						return false
					}
				}else {
					div = document.createElement('div')
				}
				div.setAttribute('id', 'AIopera')
				div.setAttribute('style', 'position: absolute;top: 24px;left: 0;box-shadow: 0 4px 8px rgba(0,0,0,.3);border-radius:10px;background: #fff;color:#000;width: 120px;line-height: 30px;z-index:99')
				var ul = document.createElement('div');
				ul.innerHTML = 'AI续写'
				ul.addEventListener('click',function(event){
					event.stopPropagation()
					that.handleAIContinuation()
				})
				div.appendChild(ul);
				var ul2 = document.createElement('div');
				ul2.innerHTML = 'AI优化'
				ul2.addEventListener('click',function(event){
					event.stopPropagation()
					that.handleAIOptimize()
				})
				div.appendChild(ul2);
				var ul3 = document.createElement('div');
				ul3.innerHTML = 'AI校对'
				ul3.addEventListener('click',function(event){
					event.stopPropagation()
					that.handleAIProofread()
				})
				div.appendChild(ul3);
				var ul4 = document.createElement('div');
				ul4.innerHTML = 'AI翻译'
				ul4.addEventListener('click',function(event){
					event.stopPropagation()
					that.handleAITranslation()
				})
				div.appendChild(ul4);
				const continuation= document.querySelector(".ql-AI");
				continuation.appendChild(div)
			},
			audioPlay() {
				var div = document.createElement('div')
				div.innerHTML = this.value
				var text = div.textContent
				const utterance = new SpeechSynthesisUtterance();
				utterance.text = text;  
				utterance.lang = 'zh-CN';  
				utterance.rate = 1.5; // 语速（0.1-10）  
				utterance.pitch = 1.0; // 音调（0-2）  
				utterance.volume = 1.0; // 音量（0-1）  
				window.speechSynthesis.speak(utterance);  
			},
			// 续写
			handleAIContinuation() {
				document.getElementById('AIopera').innerHTML = ''
				let that = this
				let loading = this.$loading({
					lock: true,
					text: 'AI续写中...',
					spinner: 'el-icon-loading',
					background: 'rgba(0, 0, 0, 0.7)'
				});
				var div = document.createElement('div')
				div.innerHTML = this.value
				var text = div.textContent + ' 请将前面的内容续写下去'
				this.$http.post('deepseek/askai', {
					ask: `${text}`,
				}).then(res => {
					if (loading) loading.close()
					that.currentIndex = 0
					typeText(res.data.data)
				});
				
				function typeText(text) {
					let quill = that.$refs[that.refname].quill;
					let length = quill.getLength();
					if (that.currentIndex < text.length) {
						quill.insertText(length - 1, text[that.currentIndex]);
						that.currentIndex++;
						that.typingInterval = setTimeout(()=>{
							typeText(text)
						}, 30); // 打字速度，单位毫秒
					} else {
						clearInterval(that.typingInterval); // 停止打字机效果
						
					}
				}
			},
			// 优化
			handleAIOptimize() {
				document.getElementById('AIopera').innerHTML = ''
				let quill = this.$refs[this.refname].quill;
				const range = quill.getSelection()
				let that = this
				if(!range.length) {
					this.$message.error('请选中需要优化的内容')
					return false
				}
				let loading = this.$loading({
					lock: true,
					text: 'AI优化中...',
					spinner: 'el-icon-loading',
					background: 'rgba(0, 0, 0, 0.7)'
				});
				var div = document.createElement('div')
				div.innerHTML = this.value
				var text = quill.getText(range.index, range.length) + ' 请帮我优化一下这段文字的内容，并只返回优化的内容'
				this.$http.post('deepseek/askai', {
					ask: `${text}`,
				}).then(res => {
					if (loading) loading.close()
					quill.deleteText(range.index, range.length)
					that.currentIndex = 0
					that.range = range
					typeText(res.data.data)
				});
				
				function typeText(text) {
					let quill = that.$refs[that.refname].quill;
					if (that.currentIndex < text.length) {
						quill.insertText(that.range.index + that.currentIndex, text[that.currentIndex]);
						that.currentIndex++;
						that.typingInterval = setTimeout(()=>{
							typeText(text)
						}, 50); // 打字速度，单位毫秒
					} else {
						clearInterval(that.typingInterval); // 停止打字机效果
						
					}
				}
			},
			// 校对
			handleAIProofread() {
				document.getElementById('AIopera').innerHTML = ''
				let quill = this.$refs[this.refname].quill;
				const range = quill.getSelection()
				let that = this
				if(!range.length) {
					this.$message.error('请选中需要校对的内容')
					return false
				}
				let loading = this.$loading({
					lock: true,
					text: 'AI校对中...',
					spinner: 'el-icon-loading',
					background: 'rgba(0, 0, 0, 0.7)'
				});
				var div = document.createElement('div')
				div.innerHTML = this.value
				var text = quill.getText(range.index, range.length) + ' 请帮我校对一下这段文字的内容，并只返回校对的内容'
				this.$http.post('deepseek/askai', {
					ask: `${text}`,
				}).then(res => {
					if (loading) loading.close()
					quill.deleteText(range.index, range.length)
					that.currentIndex = 0
					that.range = range
					typeText(res.data.data)
				});
				
				function typeText(text) {
					let quill = that.$refs[that.refname].quill;
					if (that.currentIndex < text.length) {
						quill.insertText(that.range.index + that.currentIndex, text[that.currentIndex]);
						that.currentIndex++;
						that.typingInterval = setTimeout(()=>{
							typeText(text)
						}, 50); // 打字速度，单位毫秒
					} else {
						clearInterval(that.typingInterval); // 停止打字机效果
						
					}
				}
			},
			// 翻译
			handleAITranslation() {
				document.getElementById('AIopera').innerHTML = ''
				let quill = this.$refs[this.refname].quill;
				const range = quill.getSelection()
				let that = this
				if(!range.length) {
					this.$message.error('请选中需要翻译的内容')
					return false
				}
				let loading = this.$loading({
					lock: true,
					text: 'AI翻译中...',
					spinner: 'el-icon-loading',
					background: 'rgba(0, 0, 0, 0.7)'
				});
				var div = document.createElement('div')
				div.innerHTML = this.value
				var text = quill.getText(range.index, range.length) + ' 请帮我翻译一下这段文字的内容，并只返回翻译内容'
				this.$http.post('deepseek/askai', {
					ask: `${text}`,
				}).then(res => {
					if (loading) loading.close()
					quill.deleteText(range.index, range.length)
					that.currentIndex = 0
					that.range = range
					typeText(res.data.data)
				});
				
				function typeText(text) {
					let quill = that.$refs[that.refname].quill;
					if (that.currentIndex < text.length) {
						quill.insertText(that.range.index + that.currentIndex, text[that.currentIndex]);
						that.currentIndex++;
						that.typingInterval = setTimeout(()=>{
							typeText(text)
						}, 50); // 打字速度，单位毫秒
					} else {
						clearInterval(that.typingInterval); // 停止打字机效果
						
					}
				}
			},
			onEditorBlur() {
				//失去焦点事件
			},
			onEditorFocus() {
				//获得焦点事件
			},
			onEditorChange() {
				console.log(this.value);
				//内容改变事件
				this.$emit("input", this.value);
			},
			// 富文本图片上传前
			beforeUpload() {
				// 显示loading动画
				this.quillUpdateImg = true;
			},

			uploadSuccess(res, file) {
				// res为图片服务器返回的数据
				// 获取富文本组件实例
				let quill = this.$refs[this.refname].quill;
				// 如果上传成功
				if (res.code === 0) {
					// 获取光标所在位置
					let length = quill.getSelection().index;
					// 插入图片  res.url为服务器返回的图片地址
					quill.insertEmbed(length, "image", this.baseUrl + "upload/" + res.file);
					// 调整光标到最后
					quill.setSelection(length + 1);
				} else {
					this.$message.error("图片插入失败");
				}
				// loading动画消失
				this.quillUpdateImg = false;
			},
			// 富文本图片上传失败
			uploadError() {
				// loading动画消失
				this.quillUpdateImg = false;
				this.$message.error("图片插入失败");
			}
		}
	};
</script>

<style>
	.editor {
		line-height: normal !important;
	}

	.ql-snow .ql-tooltip[data-mode="link"]::before {
		content: "请输入链接地址:";
	}

	.ql-snow .ql-tooltip.ql-editing a.ql-action::after {
		border-right: 0px;
		content: "保存";
		padding-right: 0px;
	}

	.ql-snow .ql-tooltip[data-mode="video"]::before {
		content: "请输入视频地址:";
	}

	.ql-container {
		/* height: 400px; */
	}

	.ql-snow .ql-picker.ql-size .ql-picker-label::before,
	.ql-snow .ql-picker.ql-size .ql-picker-item::before {
		content: "14px";
	}

	.ql-snow .ql-picker.ql-size .ql-picker-label[data-value="small"]::before,
	.ql-snow .ql-picker.ql-size .ql-picker-item[data-value="small"]::before {
		content: "10px";
	}

	.ql-snow .ql-picker.ql-size .ql-picker-label[data-value="large"]::before,
	.ql-snow .ql-picker.ql-size .ql-picker-item[data-value="large"]::before {
		content: "18px";
	}

	.ql-snow .ql-picker.ql-size .ql-picker-label[data-value="huge"]::before,
	.ql-snow .ql-picker.ql-size .ql-picker-item[data-value="huge"]::before {
		content: "32px";
	}

	.ql-snow .ql-picker.ql-header .ql-picker-label::before,
	.ql-snow .ql-picker.ql-header .ql-picker-item::before {
		content: "文本";
	}

	.ql-snow .ql-picker.ql-header .ql-picker-label[data-value="1"]::before,
	.ql-snow .ql-picker.ql-header .ql-picker-item[data-value="1"]::before {
		content: "标题1";
	}

	.ql-snow .ql-picker.ql-header .ql-picker-label[data-value="2"]::before,
	.ql-snow .ql-picker.ql-header .ql-picker-item[data-value="2"]::before {
		content: "标题2";
	}

	.ql-snow .ql-picker.ql-header .ql-picker-label[data-value="3"]::before,
	.ql-snow .ql-picker.ql-header .ql-picker-item[data-value="3"]::before {
		content: "标题3";
	}

	.ql-snow .ql-picker.ql-header .ql-picker-label[data-value="4"]::before,
	.ql-snow .ql-picker.ql-header .ql-picker-item[data-value="4"]::before {
		content: "标题4";
	}

	.ql-snow .ql-picker.ql-header .ql-picker-label[data-value="5"]::before,
	.ql-snow .ql-picker.ql-header .ql-picker-item[data-value="5"]::before {
		content: "标题5";
	}

	.ql-snow .ql-picker.ql-header .ql-picker-label[data-value="6"]::before,
	.ql-snow .ql-picker.ql-header .ql-picker-item[data-value="6"]::before {
		content: "标题6";
	}

	.ql-snow .ql-picker.ql-font .ql-picker-label::before,
	.ql-snow .ql-picker.ql-font .ql-picker-item::before {
		content: "标准字体";
	}

	.ql-snow .ql-picker.ql-font .ql-picker-label[data-value="serif"]::before,
	.ql-snow .ql-picker.ql-font .ql-picker-item[data-value="serif"]::before {
		content: "衬线字体";
	}

	.ql-snow .ql-picker.ql-font .ql-picker-label[data-value="monospace"]::before,
	.ql-snow .ql-picker.ql-font .ql-picker-item[data-value="monospace"]::before {
		content: "等宽字体";
	}
</style>