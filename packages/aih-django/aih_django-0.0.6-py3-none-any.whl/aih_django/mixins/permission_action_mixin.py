class PermissionActionMixin:
    default_permission_classes = None
    action_permission_classes = {}
    extend_base_permissions = True      # False overrides the base permissions

    def get_permissions(self):
        # Start with the global permission classes defined on the view
        base_permission_classes = getattr(self, 'permission_classes', [])
        
        # Get action-specific permission classes
        action_permissions = self.action_permission_classes.get(
            self.action, 
            self.default_permission_classes or []
        )
        
        # Handle permission combinations and convert to list if needed
        if action_permissions and not isinstance(action_permissions, (list, tuple)):
            action_permissions = [action_permissions]
        else:
            action_permissions = action_permissions or []
            
        # If extend_base_permissions is False and we have action-specific permissions,
        # use ONLY the action permissions
        if not self.extend_base_permissions and action_permissions:
            final_permissions = action_permissions
        else:
            # Otherwise, combine base permissions with action-specific ones
            final_permissions = base_permission_classes + action_permissions
        
        return [permission() for permission in final_permissions]

