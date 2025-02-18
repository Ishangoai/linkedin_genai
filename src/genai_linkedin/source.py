from genai_linkedin.model import generate_post_about, generate_technical_guide_about


def main():
    Option_1 = generate_post_about("the latest trends in AI and ML")
    Option_2 = generate_post_about("the trending tech news this week")
    Option_3 = generate_technical_guide_about("regression analysis in Python")

    print(Option_1)
    print("✅" * 10)
    print(Option_2)
    print("✅" * 10)
    print(Option_3)
    print("✅" * 10)


if __name__ == '__main__':
    main()
