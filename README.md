## Cách chơi:
1. Sử dụng phím điều hướng <- hoặc -> để di chuyển tàu vũ trụ(spaceship)
2. Tàu vũ trụ không được va vào các đối tượng khác(meteor, UFO, etc...). Nếu va phải, Gameover
3. Nhấn phím <space> để bắn, đạn từ tàu sẽ bắn thẳng lên từ vị trí bắn, nếu các đối tượng khác trúng đạn, đối tượng đó bị phá hủy, ta có thêm điểm(score)
4. Game có 3 level(0, 1, 2).
- Khi mới vào chơi, chúng ta sẽ ở level 0, bắn thiên thạch để tăng điểm, đạt được trên 2500 điểm thì lên level1.
- Ở level 1, các thiên thạch biến mất, chúng ta sẽ đối đầu với UFO với những vũ khí tối tân của chúng, nếu trúng phải đạn của UFO, gameover. Đạt được 4500 điểm, chúng ta sẽ lên level 2.
- Ở level 2, chúng ta sẽ chiến đấu với một cục tím tím :v khá trâu chó :v 

## Cách cài đặt
1. Cài virtualenv, git
2. Mở terminal, run ```cd ~ && git clone https://gitlab.com/it.vuonglv/pygame.git game```
2. tiếp tục: ```cd game && virtualenv -p python3 venv```
3. Chạy tiếp ```source venv/bin/activate```
4. ```pip install -r requirements.txt```
5. ```python3 shoot.py```