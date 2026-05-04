class Node: #linked list 생성
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.next = None


class HashTable:
    def __init__(self, size=101):
        self.size = size
        self.slots = [None] * size      # 각 슬롯: 연결 리스트의 head Node (또는 None)

    # ── 해시 함수 ──────────────────────────────────────────
    def _hash(self, key):
        return key % self.size #value

    # ── Linear Probing ─────────────────────────────────────
    def _probe(self, key): #key를 넣으면 slot 반환
        """key가 이미 있는 슬롯, 또는 key 삽입에 쓸 첫 빈 슬롯의 인덱스를 반환."""
        # TODO: _hash(key)를 시작점으로 순환하며 탐색하라.
        #   - 빈 슬롯(None)을 만나면 → 그 인덱스 반환  (key 없음, 삽입 가능 위치)
        #   - 슬롯의 key가 찾는 key와 같으면 → 그 인덱스 반환  (기존 key 발견)
        #   - 테이블을 한 바퀴 다 돌면 → -1 반환  (가득 참)
        slot_num = self._hash(key) #초기 index 
        for i in range(self.size): #전체 순회
            index = (slot_num+i)%self.size
            if self.slots[index] is None:
                return index
            elif self.slots[index].key == key: #[..(node),(node),]
                return index
                
        return -1
        
    #_probe(key) index만 반환
    # ── 삽입 ───────────────────────────────────────────────
    def insert(self, key, value):
        """(key, value) 쌍 삽입. 같은 key면 연결 리스트 맨 뒤에 추가."""
        # TODO: _probe로 슬롯 인덱스를 구한 뒤 아래를 처리하라.
        #   1) 슬롯이 비어 있으면 → Node(key, value)를 직접 생성해 슬롯에 저장
        #   2) 슬롯에 이미 같은 key가 있으면 → 연결 리스트 맨 끝까지 이동한 뒤
        #      마지막 노드의 next에 Node(key, value) 추가
        slot_num = self._probe(key) 
        if self.slots[slot_num] is None: # slot index 가 비어있다면 새로운 node 넣기.
            self.slots[slot_num] = Node(key,value)
        else : # 동일한 key가 있는 경우에는 끝에 추가
            cur = self.slots[slot_num]
            while cur.next is not None: # 끝까지 돌고 마지막에 추가
                cur = cur.next
            cur.next = Node(key,value)

    # ── 검색 ───────────────────────────────────────────────
    def search(self, key, value):
        """(key, value) 검색.
        성공: "{슬롯번호} {연결리스트 내 순서}"
        실패: "fail"
        """
        # TODO: _probe로 슬롯을 찾은 뒤 아래를 처리하라.
        #   1) 슬롯이 비어 있거나 key가 다르면 → "fail" 반환
        #   2) 연결 리스트를 순서대로 탐색하여 value를 찾으면 → "{idx} {순서}" 반환
        #      (첫 번째 노드가 순서 1)
        #   3) 끝까지 못 찾으면 → "fail" 반환
        slot_num = self._probe(key) 
        if self.slots[slot_num] is None : #슬롯이 비어있는경우 
            return "S fail"
        else : #slot에 value가 있으면 인덱스랑 순서 반환/ 끝까지 못찾으면 fail 반환
            cur = self.slots[slot_num]
            cnt = 1
            while cur.value != value: #value 동일 여부 판단
                if cur.next is None:
                    return "S fail"
                cur = cur.next
                cnt +=1
            # cur.value == value
            return f"S {slot_num} {cnt}"

    # ── 삭제 ───────────────────────────────────────────────
    def delete(self, key, value):
        """(key, value) 삭제.
        성공: "{슬롯번호} {다음 원소값}"  또는  "{슬롯번호} none"
        실패: "fail"
        """
        # TODO: _probe로 슬롯을 찾은 뒤 아래를 처리하라.
        #   1) 슬롯이 비어 있거나 key가 다르면 → "fail" 반환
        #   2) 헤드 노드가 삭제 대상이면:
        #        self.slots[idx] = node.next  로 헤드를 실제 제거한 뒤
        #        다음 노드가 없으면 → "{idx} none", 있으면 → "{idx} {다음값}" 반환
        #   3) 헤드 이후에서 탐색하여 node.next.value == value이면:
        #        node.next = node.next.next  로 노드 실제 제거한 뒤
        #        다음 노드가 없으면 → "{idx} none", 있으면 → "{idx} {다음값}" 반환
        #   4) 끝까지 못 찾으면 → "fail" 반환
        slot_num = self._probe(key)
        if self.slots[slot_num].key != key or self.slots[slot_num] is None:
            return "D fail"
        else : # value가 있을 경우
            cur = self.slots[slot_num]
            if cur.value == value: #head에서 삭제 대상을 찾았을 경우
                if cur.next is None : #head 한개만 있는 경우에는 아예 삭제 
                    cur = None
                    return f"D {slot_num} none"
                else : #노드 두개 이상인 경우
                    cur = cur.next
                    return f"D {slot_num} {cur.value}"
            else : #head가 아닌경우
                while cur.next.value != value : #현 node의 다음 value가 삭제 대상일 때 out
                    cur = cur.next
                    if cur.next is None:
                        return "D fail"
                #cur.next.value = value 인 쌍을 찾았을 때
                if cur.next.next is None:
                    cur.next = None
                    return f"D {slot_num} none"
                else :
                     cur.next=cur.next.next
                     return f"D {slot_num} {cur.next.value}"

    # ── 유틸리티 ───────────────────────────────────────────
    def chain_str(self, idx):
        """슬롯 idx의 연결 리스트를 문자열로 반환."""
        node = self.slots[idx]
        if node is None:
            return "(비어 있음)"
        parts = []
        while node:
            parts.append(str(node.value))
            node = node.next
        return " → ".join(parts)

    def occupied_slots(self):
        """값이 있는 슬롯 인덱스 목록 반환."""
        return [i for i in range(self.size) if self.slots[i] is not None]