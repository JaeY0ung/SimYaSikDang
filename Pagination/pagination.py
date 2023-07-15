import math

# 입력값: 데이터(list), 현재페이지, 한페이지에 보일 데이터수, pagination에 보일 페이지 수(홀수)
# 출력값: start_index, end_index, pagination_start, pagination_end, move_page_front, move_page_back
class Pagination:
    def makepagination(self, data, page, data_per_page=12, page_per_pagination=9):
        num_data = len(data) # data에 있는 정보의 개수
        total_page = math.ceil(num_data / data_per_page) # 전체 페이지 개수

        # 현재 페이지가 범위를 벗어나면 갈 수 있는 페이지로 변경
        if page < 1:
            page= 1
        elif page > total_page:
            page = total_page

        # 현재 페이지의 첫번째 데이터의 index
        start_index = (page-1) * data_per_page

        # 현재 페이지가 끝 페이지인지 아닌지 판단하여 마지막 데이터의 index 
        if page < total_page:
            end_index = page * data_per_page - 1 #전체 페이지
        else:
            end_index = num_data - 1

        # Pagination (default: 현재 페이지 숫자가 가운데)
        # 존재하는 페이지의 수가 pagination의 페이지 수보다 클 때
        if total_page >= page_per_pagination:
            if page <= 1+ page_per_pagination//2:
                pagination_start, pagination_end = 1, page_per_pagination
                move_page_front, move_page_back = False, True
            elif page <= total_page - page_per_pagination//2:
                pagination_start, pagination_end = page - page_per_pagination//2, page + page_per_pagination//2
                move_page_front, move_page_back = True, True
            else:
                pagination_start,pagination_end = total_page - page_per_pagination + 1,total_page
                move_page_front, move_page_back = True, False
        else:
            pagination_start, pagination_end = 1, total_page
            move_page_front, move_page_back = False, False

        self.start_index = start_index
        self.end_index = end_index
        self.total_page = total_page
        self.pagination_start= pagination_start
        self.pagination_end = pagination_end
        self.move_page_front = move_page_front
        self.move_page_back = move_page_back