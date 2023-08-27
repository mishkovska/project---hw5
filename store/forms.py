from django import forms

from .models import Category, Product


class AddProductForm(forms.ModelForm):

    category = forms.ModelChoiceField(label='Category', help_text='Required', queryset=Category.objects.all(), empty_label=None,
                                      widget=forms.Select(attrs={'class': 'form-select form-control'}))
    title = forms.CharField(label='Title', help_text='Required', max_length=225, widget=forms.TextInput(attrs={'class': 'form-control'}))
    description = forms.CharField(label='Description', help_text='Optional', required=False, widget=forms.Textarea(attrs={'class': 'form-control'}))
    image = forms.ImageField(label='Image', help_text='Required', widget=forms.FileInput(attrs={'class': 'form-control-file'}))
    slug = forms.SlugField(label='Slug', help_text='Required', widget=forms.TextInput(attrs={'class': 'form-control'}))
    price = forms.DecimalField(label='Price', help_text='Required', max_digits=8, decimal_places=2, widget=forms.NumberInput(attrs={'class': 'form-control'}))
    in_stock = forms.BooleanField(label='Is the product in stock?', widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))
    is_active = forms.BooleanField(label='Should the product be seen by customers?', widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))

    class Meta:
        model = Product
        fields = ('category', 'title', 'description', 'image', 'slug', 'price', 'in_stock', 'is_active')

    def clean_slug(self):
        slug = self.cleaned_data['slug']
        if Product.objects.filter(slug=slug).exists():
            raise forms.ValidationError("This slug is already in use. Please provide a unique slug.")
        return slug