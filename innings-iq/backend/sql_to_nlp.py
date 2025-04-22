def convert_result_to_text(columns, results) -> str:
    if not results:
        return "No matching data found."

    response = []
    for row in results:
        row_dict = dict(zip(columns, row))
        sentence = ", ".join(f"{key}: {value}" for key, value in row_dict.items())
        response.append(sentence)
    
    return "\n".join(response)
