import logging
import json
import azure.functions as func

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

#Bindings in declarative code(V2)
@app.route(route="CountTriggerFxn")
@app.cosmos_db_input(arg_name="inputDocument", 
                     database_name="cloudresumeDB",
                     container_name="counter",
                     #id="{Query.id}",
                     #partition_key="{id}",
                     sqlQuery = "SELECT * FROM c WHERE c.id = '1'",
                     connection="MyAccount_COSMOSDB")
@app.cosmos_db_output(arg_name="outputDocument", 
                      database_name="cloudresumeDB",
                      container_name="counter",
                      connection="MyAccount_COSMOSDB")


def GetCountValue(req: func.HttpRequest, inputDocument: func.DocumentList,
                  outputDocument: func.Out[func.Document]) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    # Simplify the counter increment and document update process
    try:
        # Assume inputDocument always has at least one document and 'count' is an int
        document = inputDocument[0]  # Directly use the first document
        document['count'] += 1  # Increment count directly

        # Update the output document
        outputDocument.set(document)

        # Simplify the response creation process
        response_body = json.dumps({"id": document['id'], "count": document['count']})
        return func.HttpResponse(body=response_body, status_code=200, mimetype="application/json")
    except Exception as e:
        logging.error(f"Error processing request: {e}")
        return func.HttpResponse("Error", status_code=500)



