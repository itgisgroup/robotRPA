Thay vì chỉ làm việc với 1 file Excel (Update_DescriptionDrawer.xlsx), bot sẽ làm việc với nhiều file Excel trong một thư mục (ví dụ: File-ChoXuLy).
Mỗi file cần xử lý sẽ có tên gốc như cũ, nhưng phía sau sẽ có tiền tố là thời gian (ví dụ: Update_DescriptionDrawer_20240610_153000.xlsx).
Sau khi hoàn thành xử lý 1 file, bot sẽ:
Copy file đó sang thư mục File-Hoanthanh.
Đổi tên file hoàn thành thành: tên gốc + _ + thời gian hoàn thành (nếu chưa có thì thêm vào, nếu đã có thì cập nhật lại thời gian hoàn thành).
Tiếp tục xử lý file tiếp theo trong danh sách.
Đánh giá khả năng thực hiện
Việc này hoàn toàn có thể làm được, chỉ cần:
Thay đổi luồng xử lý để lặp qua tất cả các file Excel trong thư mục chờ xử lý.
Sau khi hoàn thành 1 file, thực hiện thao tác copy và đổi tên như yêu cầu.
Đảm bảo bot xử lý tuần tự từng file, không bỏ sót file nào.
Gợi ý bổ sung
Nên quy định rõ định dạng tên file (ví dụ: Update_DescriptionDrawer_YYYYMMDD_HHMMSS.xlsx) để dễ nhận diện và tránh trùng lặp.
Có thể log lại quá trình xử lý từng file để dễ kiểm soát.
Nếu bạn đồng ý với hướng này, mình sẽ hướng dẫn/viết code để:
Lấy danh sách file Excel cần xử lý trong thư mục.
Xử lý từng file theo quy trình cũ.
Sau khi xong thì copy sang thư mục hoàn thành và đổi tên đúng định dạng.


Copy ID xong dán xuống dưới.
rồi mới đưa vô file excel.
mô tả rộng bỏ qua.



####
Quét tất cả các file .xlsx trong thư mục /Users/hlethanh486/Desktop/robotTH/File-ChoXuLy
Xử lý tuần tự từng file một, theo thứ tự tên file
Với mỗi file:
Thực hiện quy trình upload và xử lý như cũ
Sau khi hoàn thành, copy file sang thư mục File-Hoanthanh với tiền tố hoanthanh_DDMMYYYY_HHMMSS_
Tiếp tục với file tiếp theo
Ví dụ nếu trong thư mục File-ChoXuLy có các file:
Apply to Cập nhật luồ...
xlsx
Bot sẽ:
Xử lý file đầu tiên
Copy sang File-Hoanthanh với tên mới (ví dụ: hoanthanh_11052025_221500_Update_DescriptionDrawer_11052025_215208.xlsx)
Chuyển sang xử lý file thứ hai
Và cứ tiếp tục như vậy cho đến khi xử lý hết tất cả các file