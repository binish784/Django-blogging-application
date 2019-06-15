from rest_framework.permissions import BasePermission

class IsOwnerOrReadOnly(BasePermission):
	message='You Must be the owner of this object to update it'
	def has_object_permission(self,request,view,obj):
		return request.user == obj.user