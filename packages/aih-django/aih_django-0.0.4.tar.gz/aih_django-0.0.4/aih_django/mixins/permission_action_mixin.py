class PermissionActionMixin:
    default_permission_classes = None   # Defautl Permissions (minimum)
    action_permission_classes = {}      # Define dictionary of permissions for actions

    def get_permissions(self):
        # Start with the global permission classes defined on the view
        base_permission_classes = getattr(self, 'permission_classes', [])
        
        # Get additional permission classes for the current action
        action_permissions = self.action_permission_classes.get(
            self.action, 
            self.default_permission_classes or []
        )
        
        # Handle permission combinations and convert to list if needed
        if action_permissions and not isinstance(action_permissions, (list, tuple)):
            action_permissions = [action_permissions]
        else:
            action_permissions = action_permissions or []
            
        # Combine base permissions with action-specific ones
        # This ensures base permissions are always required
        combined_permissions = base_permission_classes + action_permissions
        
        return [permission() for permission in combined_permissions]

