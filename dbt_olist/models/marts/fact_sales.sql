select
    o.order_id,
    o.customer_id,
    oi.product_id,
    oi.seller_id,

    cast(o.order_purchase_timestamp as date)
        as purchase_date,

    oi.price,
    oi.freight_value,

    oi.price + oi.freight_value
        as sales_amount

from {{ ref('stg_orders') }} o

join {{ ref('stg_order_items') }} oi
    on o.order_id = oi.order_id