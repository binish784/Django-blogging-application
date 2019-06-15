from django import forms
from .models import post,comment


from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout,HTML,Submit,Field
from crispy_forms.bootstrap import FormActions,PrependedText,Div

class PostForm(forms.ModelForm):

	class Meta:	
		model=post
		fields=['title','content','image']

	def __init__(self,*args,**kwargs):
		super(PostForm,self).__init__(*args,**kwargs)
		self.helper=FormHelper()
		self.fields['title'].label=False
		self.fields['content'].label=False
		self.helper.form_method="POST"
		self.helper.layout=Layout(
			Field('title',placeholder='Blog Title Goes here'),
			Field('content',placeholder='Content Goes here'),
			Field('image'),
			FormActions(
				Submit('save','Create Post',css_class='btn btn-primary'),
				)

			)

class CommentForm(forms.ModelForm):
	class Meta:
		model=comment
		fields=['comment_text']

	def __init__(self,*args,**kwargs):
		super(CommentForm,self).__init__(*args,**kwargs)
		self.helper=FormHelper()
		self.fields['comment_text'].label=False
		self.form_method="POST"
		self.helper.layout=Layout(
			Div(
				Div(PrependedText('comment_text','#',placeholder='Comment Goes here //'),css_class='col-md-10'),
				Div(FormActions(Submit('save','Comment')),css_class='col-md-2')
			,css_class='row'))