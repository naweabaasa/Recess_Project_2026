## 🗄️ Database Migration Order

To ensure correct foreign key relationships, the database tables must be migrated in the following dependency order:

**Layer 0: Independent Tables (No Foreign Keys)**
1. `permissions`
2. `roles`
3. `categories`
4. `brands`
5. `customers`

**Layer 1: Tables Referencing Layer 0**
6. `role_permissions` (depends on `roles`, `permissions`)
7. `admins` (depends on `roles`)
8. `orders` (depends on `customers`)
9. `shopping_carts` (depends on `customers`)

**Layer 2: Tables Referencing Layer 0 & Layer 1**
10. `products` (depends on `categories`, `brands`, `admins`)
11. `cart_items` (depends on `shopping_carts`, `products`)
12. `order_items` (depends on `orders`, `products`)
13. `deliveries` (depends on `orders`)
