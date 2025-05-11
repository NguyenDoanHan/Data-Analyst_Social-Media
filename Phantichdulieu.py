

import pandas as pd
import matplotlib.pyplot as plt

#1.Định nghĩa các trường thông tin của sheet Dữ liệu
"""đọc và hiện thị dữ liệu"""
df_RA = pd.read_excel("Data Analyst_Social Media.xlsx")
print("Thông tin cột dữ liệu:")
print(df_RA.columns)
print(df_RA.info())
print(df_RA.describe())


#2.Kiểm tra và xử lý lại sắc thái (sentiment)
print(df_RA['Sentiment'].value_counts(dropna=False))

#3. Xử lý dữ liệu mẫu
print("giá trị thiếu:")
print(df_RA.isnull().sum())
print("làm sạch dữ liệu")
df_RA = df_RA.dropna()
print(df_RA.shape)
print("4 khía cạnh")

def classify_topic(text):
    text = str(text).lower()
    if 'tcbs' in text and any(keyword in text for keyword in ['thương hiệu', 'uy tín', 'hình ảnh']):
        return 'Thương hiệu'
    elif any(keyword in text for keyword in ['sản phẩm', 'dịch vụ', 'app', 'ứng dụng']):
        return 'Sản phẩm'
    elif any(keyword in text for keyword in ['khuyến mãi', 'giảm giá', 'ưu đãi', 'tặng']):
        return 'Chương trình khuyến mãi'
    else:
        return 'Khác'

df_RA['Topic_Category'] = df_RA['Title'].apply(classify_topic)
print(df_RA['Topic_Category'].value_counts())


#4. Thống kê các chỉ số
print("Thông kê các chỉ số")
df_RA['Like'] = pd.to_numeric(df_RA['Like'], errors='coerce')
df_RA['Comments'] = pd.to_numeric(df_RA['Comments'], errors='coerce')
df_RA['Shares'] = pd.to_numeric(df_RA['Shares'], errors='coerce')
df_RA['Engagement'] = df_RA['Like'] + df_RA['Comments'] + df_RA['Shares']
print(df_RA[['Like', 'Comments', 'Shares', 'Engagement']].describe())

#5. Vẽ biểu đồ xu hướng thảo luận (mention) và tương tác (egagement) theo thời gian. Cho thấy được lượng thảo luận và tương tác mỗi ngày là bao nhiêu.
df_RA['Created Date'] = pd.to_datetime(df_RA['Created Date'], errors='coerce')
df_RA = df_RA.dropna(subset=['Created Date'])

df_RA['Post'] = 1
df_RA['Mention'] = df_RA['Post'] +df_RA['Comments']
mention_by_date = df_RA.groupby(df_RA['Created Date'].dt.date)['Mention'].sum()
mention_by_date.plot(kind='line', figsize=(10,5), color='blue')
plt.title('Xu hướng thảo luận theo thời gian (Mention)')
plt.xlabel('Ngày')
plt.ylabel('Mention (post + comment)')
plt.xticks(rotation=75)
plt.tight_layout()
plt.grid()
plt.savefig("Mention_Trend.png")
plt.show()


engagement_by_date = df_RA.groupby(df_RA['Created Date'].dt.date)['Engagement'].sum()
engagement_by_date.plot(kind='line', figsize=(10,5), color='green')
plt.title('Tương tác theo thời gian (Engagement)')
plt.xlabel('Ngày')
plt.ylabel('Engagement (like + comment + share)')
plt.xticks(rotation=75)
plt.tight_layout()
plt.grid()
plt.savefig("Engagement_Trend.png")
plt.show()

#6. Vẽ biểu đồ thể hiện tỉ lệ thảo luận trên từng nền tảng (platforms)
platform_mentions = df_RA.groupby('Platform')['Mention'].sum()
platform_mentions = df_RA.groupby('Platform')['Mention'].sum()
platform_mentions.plot(kind='bar', figsize=(8,5), color='purple')
plt.title('Tỉ lệ thảo luận trên từng nền tảng (platforms)')
plt.xlabel('Nền tảng')
plt.ylabel('Mentions')
plt.tight_layout()
plt.grid()
plt.savefig("Platform_Mentions.png")
plt.show()

#7 . Vẽ biểu đồ thể hiện tỉ lệ sắc thái thảo luận (sentiment)
sentiment_counts = df_RA['Sentiment'].value_counts()
sentiment_counts.plot(kind='bar', figsize=(8, 5), color='skyblue')
plt.title('Phân bố sắc thái thảo luận (Sentiment)')
plt.xlabel('Sentiment')
plt.ylabel('Số lượng')
plt.tight_layout()
plt.grid()
plt.savefig("Sentiment_Distribution.png")
plt.show()

#8. Top 5 chủ đề (nội dung) có nhiều thảo luận nhất trong bảng dữ liệu
df_RA_Top5 = df_RA.groupby('Title')['Mention'].sum().sort_values(ascending=False)
print(df_RA_Top5.head(5))

df_RA_Top5.plot(kind='barh', figsize=(10,5), color='orange')
plt.title('Top 5 Chủ đề được thảo luận nhiều nhất')
plt.xlabel('Số lượt thảo luận')
plt.ylabel('Tiêu đề')
plt.tight_layout()
plt.grid()
plt.savefig("df_RA_Top5.png")
plt.show()

#9. Đánh giá chung về dữ liệu
print("Tổng số bài viết:", df_RA.shape[0])
print("Tổng số tác giả:", df_RA['Author'].nunique())
print("Tỉ lệ các sentiment:")
print((df_RA['Sentiment'].value_counts(normalize=True) * 100).round(2))
print("Tổng engagement trung bình mỗi bài:", df_RA['Engagement'].mean().round(2))

#Xuất Bảng excel số liệu đã phân tích/tổng hợp
df_RA.to_excel("DuLieu_PhanTich.xlsx", index=False)
mention_by_date.to_excel("Mention_by_Date.xlsx")
engagement_by_date.to_excel("Engagement_by_Date.xlsx")
platform_mentions.to_excel("Mentions_by_Platform.xlsx")
sentiment_counts.to_excel("Sentiment_Counts.xlsx")
df_RA_Top5.to_excel("Top5_Title.xlsx")
