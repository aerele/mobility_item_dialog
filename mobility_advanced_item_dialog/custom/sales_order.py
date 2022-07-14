from unittest import result
import frappe
from frappe.model.document import Document
from json import loads
from erpnext.stock.doctype.batch.batch import get_batch_qty
class SalesInvoice(Document):
    pass

@frappe.whitelist()
def get_item_details(filters=None):
    filters=loads(filters)
    if(filters["item_code"]!="" or  filters["brand"]!=""):
        condition=""
        if(filters["item_code"]==""):
            condition=("and brand= '{0}' ".format(filters["brand"]))
        elif(filters["brand"]==""):
            condition=("and name= {0}".format(filters["item_code"]))
        else:
            condition=("and name= {0} and brand= '{1}' ".format(filters["item_code"],filters["brand"]))
        result=frappe.db.sql("""Select item_code as 'Item Code', item_name as 'Item Name', brand as Brand ,has_batch_no as 'Has Batch No'
        from `tabItem` where has_batch_no= 1 {0}  and disabled= 0 """.format(condition),as_dict=True)
        result_value=[]
        length=len(result)
        for i in range(0,length):
            batch_values=get_qnt_on_batch_warehouse(str(result[i]["Item Code"]),filters["warehouse"],filters["price_list"])
            if(filters["exclude_zero_quantity"]==0):
                for j in range(len(batch_values)):
                    result_value.append({"Item Code":str(result[i]["Item Code"]),"Item Name":str(result[i]["Item Name"]),"Brand":str(result[i]["Brand"]),"Production Year":batch_values[j]["production_year"],"Rate":batch_values[j]["rate"],"Qty":batch_values[j]["qty"],"Batch":batch_values[j]["batch_no"]})
            else:
                for j in range(len(batch_values)):
                    if(batch_values[j]["qty"]!=0):
                        result_value.append({"Item Code":str(result[i]["Item Code"]),"Item Name":str(result[i]["Item Name"]),"Brand":str(result[i]["Brand"]),"Production Year":batch_values[j]["production_year"],"Rate":batch_values[j]["rate"],"Qty":batch_values[j]["qty"],"Batch":batch_values[j]["batch_no"]})
        return {"values": result_value}
    return{"values":[]}
def get_qnt_on_batch_warehouse(item,warehouse,price_list):
    batch=[]
    all_batch=frappe.db.get_list("Batch",{"item":item,"disabled":0})
    for batchs in all_batch:
        batch_values=get_batch_qty(warehouse=warehouse,batch_no=batchs["name"])
        batch.append({"production_year":(frappe.db.get_value("Batch",{"name":batchs["name"],"item":item},"production_year")),
        "qty":batch_values,
        "rate":(frappe.db.get_value("Item Price",{"item_code":item,"price_list":price_list,"batch_no":batchs["name"]},"price_list_rate")),
        "batch_no":batchs["name"]
        })
    return batch