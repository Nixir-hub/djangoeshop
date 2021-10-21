from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import DetailView, UpdateView, DeleteView, FormView, ListView
from accounts_app.form import PasswordChangeForm, SignUpForm, EditProfilForm, EditUserForm
from eshopp_app.models import Profile, Cart, Discount


# 2 testy zrobione
class UserProfilView(LoginRequiredMixin, DetailView):
    model = User
    template_name = "profil_detail.html"

    def get_object(self, queryset=None):
        self.object = self.request.user
        return self.object


# test 1 get 1 post
class CreateUser(View):

    def get(self, request):
        form = SignUpForm()
        return render(request, "registration/signup.html", {"form": form})

    def post(self, request):
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = User.objects.create(username=request.POST.get("username"),
                                       first_name=request.POST.get("first_name"),
                                       last_name=request.POST.get("last_name"),
                                       email=request.POST.get("email"))
            user.set_password(request.POST.get("password1"))
            user.save()
            discount = Discount.objects.create(user=User.objects.get(id=user.id), amount=0.3)
            discount.save()
            Cart.objects.create(
                user=User.objects.get(id=user.id),
                discount=Discount.objects.get(user=User.objects.get(id=user.id))
                                ).save()
            Profile.objects.create(user=User.objects.get(id=user.id)).save()
            return redirect("/logout")
        return render(request, 'registration/signup.html', {'form': form})


# 2 testy na get 1 test z postem
class DeleteUserView(LoginRequiredMixin, DeleteView):
    model = User
    template_name = "del_form.html"
    success_url = "/"

    def get_object(self, queryset=None):
        self.object = self.request.user
        return self.object


# 3 testy 2 get, 1 post
class EditUserProfil(LoginRequiredMixin, UpdateView):
    model = Profile
    template_name = "form.html"
    form_class = EditProfilForm
    success_url = "/profil_details/"

    def get_object(self, queryset=None):
        self.object = self.request.user.profile
        return self.object


# 3 testy 2 get 1 post
class EditUserData(LoginRequiredMixin, UpdateView):
    model = User
    fields = ("first_name", "last_name")
    template_name = "form.html"
    template_class = EditUserForm
    success_url = "/profil_details/"

    def get_object(self, queryset=None):
        self.object = self.request.user
        return self.object


# 3 testy 2 get 1 post
class PasswordChangeView(LoginRequiredMixin, FormView):
    model = User
    form_class = PasswordChangeForm
    success_url_reverse_lazy = "/profil_details/"


# 3 testy
class UserListView(PermissionRequiredMixin, ListView):
    permission_required = "eshopp_app.view_payment"
    model = User
    fields = "groups"
    template_name = "user_list.html"


# 3 testy 2 get 1 post
class EditUserPermissionView(PermissionRequiredMixin, UpdateView):
    permission_required = "eshopp_app.view_payment"
    model = User
    fields = ("groups",)
    template_name = "form.html"
    success_url = "/site_moderator/"


# 3 tests
class AdminView(PermissionRequiredMixin, View):
    permission_required = "eshopp_app.view_payment"

    def get(self, request):
        return render(request, "admin_list_view.html")
