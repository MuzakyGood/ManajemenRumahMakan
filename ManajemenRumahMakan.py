MenuMakananMinuman = (
    ("Nasi Goreng", 5),
    ("Mie Goreng", 3),
    ("Telur Dadar", 3),
    ("Sop Ayam", 4),
    ("Ayam Goreng", 5),
    ("Ayam Geprek", 7),
    ("Pizza", 25),
    ("Air putih", 1),
    ("Teh", 2),
    ("Kopi", 2),
    ("Jus", 4)
)

def ShowMenus():
    print("-" * 35)
    print(f"{" ":<3}DAFTAR MENU MAKANAN & MINUMAN")
    print("-" * 35)
    for i, (nama_menu, waktu) in enumerate(MenuMakananMinuman):
        print(f"[{i + 1:>2}] {nama_menu:<15} {waktu:>2} minutes")
    print("-" * 35)
    print()

def ShowSkilledChef():
    rateChef = ("Magang", "Pemula", "Menengah", "Profesional", "Artificial Intellegent")

    print()

    print("-" * 35)
    for i in range(0, 5):
        print(f"{i+1} -> {rateChef[i]}")
    print("-" * 35)

class Pengunjung:
    def __init__(self, name: str, process: int, arrivalTime: int):
        self._namaPengunjung = name
        self._namaPesanan = MenuMakananMinuman[process - 1][0]
        self._prosesPesanan = MenuMakananMinuman[process - 1][1]
        self._waktuDatang = arrivalTime

    def getName(self) -> str:
        return self._namaPengunjung
    
    def getFoodName(self) -> str:
        return self._namaPesanan

    def getProcess(self) -> int:
        return self._prosesPesanan
    
    def getArrivalTime(self) -> int:
        return self._waktuDatang
    
    def setName(self, name: str):
        self._namaPengunjung = name

    def setNamaPesanan(self, makanan: str):
        self._namaPesanan = makanan

    def setProcess(self, process: int):
        self._prosesPesanan = MenuMakananMinuman[process - 1][1]

    def setArrivalTime(self, arrive: int):
        self._waktuDatang = arrive
        
    def __str__(self):
        return f"{self._namaPengunjung} ordering ({self._namaPesanan}) process ({self._prosesPesanan} minutes) arrival time ({self._waktuDatang} minutes)"

class Stack:
    def __init__(self):
        self.top = None
        self.size = 0

    def getSize(self) -> int:
        return self.size

    def isEmpty(self) -> bool:
        return self.size == 0

    def push(self, value):
        node = Node(value)
        node.next = self.top  
        self.top = node       
        self.size += 1

    def pop(self):
        if self.isEmpty():
            raise Exception("Popping from an empty stack!")
        remove = self.top
        self.top = self.top.next  
        self.size -= 1
        return remove.value

class Node:
    def __init__(self, value):
        self.value = value
        self.next = None

class Queue:
    def __init__(self):
        self.head = None
        self.tail = None 
        self.size = 0
    
    def getSize(self) -> int:
        return self.size

    def isEmpty(self) -> bool:
        return self.size == 0
    
    def peek(self):
        if self.isEmpty():
            raise Exception("Peeking from an empty queue!")
        return self.head.value
    
    def enqueue(self, value):
        node = Node(value)
        if self.isEmpty():
            self.head = node
            self.tail = node
        else:
            self.tail.next = node  
            self.tail = node
        self.size += 1

    def dequeue(self):
        if self.isEmpty():
            raise Exception("Dequeue from an empty queue!")
        
        remove = self.head         
        self.head = self.head.next 
        
        if self.head is None:
            self.tail = None
            
        self.size -= 1
        return remove.value
    
    def at(self, index):
        if index < 0 or index >= self.size:
            raise IndexError("Index out of bounds!")

        current = self.head
        current_index = 0
        
        while current is not None:
            if current_index == index:
                return current.value
            current = current.next
            current_index += 1
            
        return None

class RoundRobin:
    def __init__(self, time_quantum: int):
        self.quantum = time_quantum

    def _cookingStatus(self, cooking: str) -> str:
        return "menyiapkan" if (cooking == "Air putih" or cooking == "Teh" or cooking == "Kopi" or cooking == "Jus") else "memasak" 

    def runSimulation(self, daftar_pelanggan: Queue):
        print("\n" + "="*10 + " PROSES MEMASAK " + "="*10)
        
        waktu_global = 0
        ready_queue = Queue()
        tumpukan_piring_kotor = Stack()
        
        sisa_waktu = {}
        sudah_masuk_antrean = [False] * daftar_pelanggan.getSize()
        jumlah_selesai = 0
        total_pelanggan = daftar_pelanggan.getSize()

        for i in range(total_pelanggan):
            p = daftar_pelanggan.at(i)
            sisa_waktu[p] = p.getProcess()

        while jumlah_selesai < total_pelanggan:
            
            for i in range(total_pelanggan):
                p = daftar_pelanggan.at(i)
                if p.getArrivalTime() <= waktu_global and not sudah_masuk_antrean[i]:
                    ready_queue.enqueue(p)
                    sudah_masuk_antrean[i] = True

            if ready_queue.isEmpty():
                menit_berikutnya = None
                for i in range(total_pelanggan):
                    if not sudah_masuk_antrean[i]:
                        p = daftar_pelanggan.at(i)
                        if menit_berikutnya is None or p.getArrivalTime() < menit_berikutnya:
                            menit_berikutnya = p.getArrivalTime()
                
                if menit_berikutnya is not None:
                    print(f"[Menit {waktu_global:>2} - {menit_berikutnya:>2}] Koki sedang santai menunggu pelanggan datang...")
                    waktu_global = menit_berikutnya
                    continue

            pelanggan_aktif = ready_queue.dequeue()
            
            durasi_masak = min(self.quantum, sisa_waktu[pelanggan_aktif])
            
            statusCook = self._cookingStatus(pelanggan_aktif.getFoodName())
            print(f"[Menit {waktu_global:>2}] Koki {statusCook} {pelanggan_aktif.getFoodName()} milik {pelanggan_aktif.getName()} ({durasi_masak} mnt). Sisa sisa waktu: {sisa_waktu[pelanggan_aktif] - durasi_masak} mnt")
            
            waktu_global += durasi_masak
            sisa_waktu[pelanggan_aktif] -= durasi_masak

            for i in range(total_pelanggan):
                p = daftar_pelanggan.at(i)
                if p.getArrivalTime() <= waktu_global and not sudah_masuk_antrean[i]:
                    ready_queue.enqueue(p)
                    sudah_masuk_antrean[i] = True

            if sisa_waktu[pelanggan_aktif] > 0:
                ready_queue.enqueue(pelanggan_aktif)
            else:
                print(f"\n{pelanggan_aktif.getFoodName()} milik {pelanggan_aktif.getName()} MATANG & DIANTARKAN! (Menit ke-{waktu_global})\n")
                jumlah_selesai += 1
                tumpukan_piring_kotor.push(pelanggan_aktif)

        print("=" * 50)
        print(f"SEMUA PESANAN SELESAI DISAJIKAN PADA MENIT KE-{waktu_global}!")

        print("\n" + "-"*12 + " SESI BERSIH-BERSIH DAPUR " + "-"*12)
        print("Koki mengambil piring kotor dari tumpukan paling atas:")
        while not tumpukan_piring_kotor.isEmpty():
            pelanggan_selesai = tumpukan_piring_kotor.pop() 
            print(f"Koki mencuci piring bekas makan {pelanggan_selesai.getName()} (Menu: {pelanggan_selesai.getFoodName()})")
        print("-" * 65)

if __name__ == "__main__":
    q = Queue()
    pelanggan = Queue()

    print("\t\tAPLIKASI MANAJEMEN RUMAH MAKAN\n")

    try:
        jumlahPengunjung = int(input("Masukan jumlah pengunjung: "))
    except ValueError as e:
        print("Error: Tipe data yang di masukan harus berupa angka!")
        exit(1)

    for i in range(jumlahPengunjung):
        while True:

            ShowMenus()
            
            namaPengunjung = input(f"Nama pengunjung ke-{i+1}: ")
            if namaPengunjung == "":
                print("\nError: Data yang di masukan tidak boleh kosong!\n")
                continue
            else:
                break
        
        while True:
            try:
                selectMakanan = int(input("Pilih nomor makanan (1/2/etc): "))
                if selectMakanan > 0 and selectMakanan <= len(MenuMakananMinuman):
                    break
                else:
                    print("\nError: Menu tidak valid!\n")
                    continue
            except ValueError as e:
                print("\nError: Tipe data yang di masukan harus berupa angka!\n")
                continue
    
        while True:
            try:
                arrival = int(input("Masukan waktu datang pelanggan: "))
                break
            except ValueError as e:
                print("\nError: Tipe data yang di masukan harus berupa angka!\n")
                continue

        pelanggan.enqueue(Pengunjung(namaPengunjung, selectMakanan, arrival))

    print()
    print("=" * 75)
    for i in range(pelanggan.getSize()):
        print(f"{i+1}. {pelanggan.at(i)}")
    print("=" * 75)

    ShowSkilledChef()

    while True:
        try:
            skilledChef = int(input("Masukan seberapa ahli koki (1-5): "))
            if skilledChef <= 0 or skilledChef > 5:
                print("Error: harus lebih besar dari 0 dan lebih kecil dari 6!")
                continue
            break
        except ValueError:
            print("Error: Harus berupa angka!")

    rr = RoundRobin(skilledChef)
    rr.runSimulation(pelanggan)