##################################################
##################################################
"""               NGUYEN CONG HUY              """
####    ##################   #####    ####    ####
####    ##################   ######   ####    ####
####          ######         #### ##  ####    ####
####          ######         ####  ## ####    ####
####          ######         ####   ######    ####
####          ######         ####   ######    ####
####                TOFU NGUYEN               ####
##################################################
##################################################

###########################################################################
#### Module's name: Basic Operations Solving                           ####
#### Programmer: Nguyen Cong Huy (Nickname: Tofu Nguyen)               ####
#### Finished date: Sunday, December 29, 2024                          ####
###########################################################################

def basicOperations(text):
    # Define a dictionary to map basic Vietnamese numbers to digits
    number_map = {
        "không": 0, "một": 1, "hai": 2, "ba": 3, "bốn": 4,
        "năm": 5, "sáu": 6, "bảy": 7, "tám": 8, "chín": 9,
        "mười": 10, "mươi": 10, "trăm": 100, "nghìn": 1000
    }

    # Function to convert Vietnamese text-based numbers to numeric values
    def text_to_number(text):
        words = text.split()
        total = 0
        current = 0
        for word in words:
            if word in number_map:
                value = number_map[word]
                if value == 10 and current != 0:  # Handle "mươi"
                    current *= value
                elif value >= 100:  # Handle "trăm", "nghìn"
                    current = max(1, current) * value
                    total += current
                    current = 0
                else:
                    current += value
            elif word in ["linh", "lẻ"]:  # Skip "linh" and "lẻ"
                continue
            else:  # Finalize the current number
                total += current
                current = 0
        total += current
        return total

    # Replace Vietnamese text-based numbers with their numeric equivalents
    def replace_vietnamese_numbers(text):
        words = text.split()
        replaced_words = []
        temp = []
        for word in words:
            if word in number_map or word in ["linh", "lẻ"]:
                temp.append(word)
            else:
                if temp:
                    replaced_words.append(str(text_to_number(" ".join(temp))))
                    temp = []
                replaced_words.append(word)
        if temp:
            replaced_words.append(str(text_to_number(" ".join(temp))))
        return " ".join(replaced_words)

    # Preprocess the input text
    text = replace_vietnamese_numbers(text)

    # Input processing - Removing unnecessary items
    text = text.replace("=", "")
    text = text.replace(" bằng", "")
    text = text.replace(" bao nhiêu", "")
    text = text.replace("?", "")
    text = text.replace(" mấy", "")

    # Input processing - replacing text with mathematical symbols
    text = text.replace("cộng", "+")
    text = text.replace("trừ", "-")
    text = text.replace("nhân", "*")
    text = text.replace("chia", "/")
    text = text.replace("chia cho", "/")
    text = text.replace("x", "*")

    # Try to calculate the operations
    try:
        result = eval(text)
        if result == "None" and "/" in text:
            return "Tôi không thể tính được. Phép toán chia cho 0 không hợp lệ."
        return f"Kết quả là {result}"
    # If there's an error or cannot calculate it, return a response
    except:
        return "Thành thật xin lỗi! Tôi không hiểu phép toán mà bạn đưa vào! Mong bạn thông cảm vì sự bất tiện này."

# Test the function
# print(basicOperations("hai mươi ba cộng bốn mươi năm bằng bao nhiêu"))
# print(basicOperations("một trăm linh năm trừ sáu mươi ba bằng bao nhiêu"))
# print(basicOperations("một nghìn hai trăm lẻ bảy nhân hai bằng bao nhiêu"))

###########################################################################
####                                                                   ####
####                © 2024 Mary Assistant | Tofu Nguyen                ####
####                                                                   ####
###########################################################################