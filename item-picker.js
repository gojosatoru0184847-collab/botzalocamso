(()=>{
 'use strict';
 const fields=['hair','top','bottom','shoes','mask','face','action'];
 // Only these texture thumbnails exist. Never pretend an action has a real icon.
 const supplied=new Set(["hair-lang-khach-tim","hair-soi-cong-nghe","hair-hac-tinh","hair-tieu-tien","hair-duong-pho-cao-cap","hair-trai-ngo-ngao","hair-duong-pho","hair-bich-vang","hair-hac-anh-tinh-ha","hair-dao-si-do","hair-lan-song-nang-dong","hair-ghet-su-gia-doi","hair-phu-thuy","hair-bushido","hair-bushido-cao-cap","hair-su-gia-ac-ma","hair-xoa","hair-chien-binh-tho","hair-soai-ca-cuong-thi","hair-tho-black","hair-quai-nhan-hu-khong","hair-tho-white","hair-tho-quay","hair-tho-red","hair-tho-thien-ha","hair-tho-pink","hair-tho-purple","hair-tho-yellow","hair-alien-x","hair-caption-american","hair-titan-tien-cong","hair-titan-thiet-giap","hair-nguoi-nhen","hair-tho-san-huyet-quy","hair-mordecai","hair-nguoi-nhen-full-set","hair-ky-hoa","hair-phac-thao","hair-chieu-mua","hair-bach-tuoc-ca","hair-bom","hair-chien-binh-tuyet-bang","hair-chien-than-esports","hair-chien-than-phong-cach-tim","hair-chien-than-phong-cach-vang","hair-chien-than-phong-cach-xanh","hair-chien-than-phong-cach-do","top-ve-binh-tinh-tu","top-quy-lua","top-qua-den","top-cuop-bien-nam","top-dau-si-huyen-thoai","top-nguoi-choi-squid","top-thu-linh-binh-doan","top-thiet-quyen","top-da-bong-anh","top-lv-up","top-da-bong-den","top-tho-quay","top-peru","top-ao-bong-bi","top-da-bong-argentina","top-da-bong-duc","top-co-rua-trang","top-bong-ma-phia-tay","top-duong-pho","top-cau-thu-tay-dai","top-duong-pho-cao-cap","top-co-rua-den","top-gojo","top-hello-kitty","top-hello-kitty-xanh","top-vo-dien-loi-than","top-bushido","top-bushido-cao-cap","top-da-biker","top-xoa","top-chien-binh-tho","top-trai-ngo-ngao","top-quai-nhan-hu-khong-black","top-quai-nhan-hu-khong","top-quai-nhan-hu-khong-white","top-quai-nhan-hu-khong-blue","top-tho-neon","top-tho-red","top-tho-black","top-tho-pink","top-tho-purple","top-tho-yellow","top-thich-khach-kim-long","top-ngu-thanh-phong","top-thich-khach-bong-dem","top-titan-tien-cong","top-titan-thiet-giap","top-nguoi-nhen","top-hac-ginh","top-da-bong-brazill","top-3-lo-trang","bottom-thien-than-thanh-thien","bottom-ngu-thanh-phong","bottom-sooc-den","bottom-ve-binh-tinh-tu","bottom-phong-cach-street","bottom-bong-chay","bottom-thien-than-hoang-kim","bottom-tham-hiem-hong-thien","bottom-tre-trau","bottom-tham-hiem-loi-lac","bottom-pyjama-gau-truc","bottom-angelic-neon","bottom-bang-cuop-dem","bottom-duong-pho","bottom-chien-binh-tho","bottom-duong-pho-cao-cap","bottom-dong-phuc-anh","bottom-gojo","bottom-hello-kitty","bottom-hello-kitty-xanh","bottom-vo-dien-loi-than","bottom-bushido","bottom-bushido-cao-cap","bottom-ky-hoi","bottom-xoa","bottom-dau","bottom-quai-nhan-hu-khong-black","bottom-quai-nhan-hu-khong","bottom-quai-nhan-hu-khong-white","bottom-quai-nhan-hu-khong-blue","bottom-dau-si-tho","bottom-tho-red","bottom-tho-thien-ha","bottom-tho-pink","bottom-tho-purple","bottom-tho-yellow","bottom-hac-tinh","bottom-hoa-quyen-su","bottom-nguoi-nhen","bottom-nguoi-choi-squid-game","bottom-dau-sy-huyen-thoai","bottom-ac-quy","bottom-boy-pho","bottom-bo-rach-roi","shoes-dep-di-bien","shoes-hacker","shoes-dep-heo-u","shoes-bong-ro","shoes-thanh-phong","shoes-ca-sau","shoes-ca-map","shoes-hello-kitty","shoes-vo-dien-loi-than","shoes-bushido-cao-cap","shoes-bong-gau-do","shoes-xoa","shoes-chien-binh-tho","shoes-bushido","shoes-dau-si-tho","shoes-tho-black","shoes-nguoi-nhen","shoes-hac-tinh","shoes-hoang-de-hai-huoc","shoes-he-vui-ve","shoes-hoi-tho-mua-he","shoes-hoa-quyen-su","shoes-thien-than","shoes-to-ong","shoes-dau-rang","shoes-di-bien-vang","mask-su-gia-ac-ma","mask-ma-bup-be-nham-thach","mask-noel","mask-chien-than-dung-nham","mask-chien-than","mask-ma-bup-be","mask-hac-anh-tinh-ha","mask-hac-tinh","mask-tien-si-con-trung","mask-vo-dien-loi-than","mask-bushido","mask-bushido-cao-cap","mask-xoa","mask-trai-ngo-ngao","mask-titan-tien-cong","mask-titan-thiet-giap","mask-anbu","mask-mordecai","mask-bang-che-mat-quan-lot","mask-bang-che-mat-ao-lot","mask-ffwc-2025","mask-ffws-2025","mask-hello-kitty","face-tiec-cuong-loan","face-xoa"]);
 const pickers=new Map();let active=null;
 const dialog=document.createElement('dialog');dialog.className='item-picker-dialog';
 dialog.innerHTML='<div class="item-picker-head"><strong id="item-picker-title">Chọn đồ</strong><button type="button" aria-label="Đóng">✕</button></div><input class="item-picker-search" type="search" placeholder="Tìm trang phục…" aria-label="Tìm trang phục"><p class="item-picker-note" id="item-picker-note">Ảnh xem nhanh từ texture gốc; không phải icon trong game.</p><div class="item-picker-list" role="listbox" aria-labelledby="item-picker-title"></div>';
 document.body.append(dialog);
 const list=dialog.querySelector('.item-picker-list');
 const search=dialog.querySelector('input');
 const title=dialog.querySelector('strong');
 const note=dialog.querySelector('#item-picker-note');
 function initials(value){
  const s=(value||'').trim();
  if(s.length<=4)return s.toUpperCase();
  const words=s.split(/\s+/).filter(Boolean);
  return words.length===1?words[0].slice(0,3).toUpperCase():words.slice(0,2).map(w=>w[0].toUpperCase()).join('');
 }
 function fallback(field,option){
  const el=document.createElement('span');el.className='item-picker-art item-picker-placeholder';
  const id=option?.dataset?.itemId||field;
  let hash=0;for(const c of id)hash=((hash*31+c.charCodeAt(0))>>>0);
  const hue=hash%360;
  el.style.background='linear-gradient(150deg,hsl('+hue+' 38% 30%),hsl('+((hue+30)%360)+' 40% 13%))';
  el.textContent=initials(option?.textContent)||'—';
  el.title='Chưa có ảnh riêng trong dữ liệu';el.setAttribute('aria-hidden','true');
  return el;
 }
 function art(field,option){
  const id=option?.dataset?.itemId;
  if(!supplied.has(id))return fallback(field,option);
  const el=new Image();el.className='item-picker-art';
  el.src='./assets/item-icons/'+id+'.webp';
  el.alt='';el.loading='lazy';el.decoding='async';
  el.addEventListener('error',()=>el.replaceWith(fallback(field,option)),{once:true});
  return el;
 }
 function sync(){
  for(const [field,{select,button}] of pickers){
   const option=select.selectedOptions[0];button.replaceChildren(art(field,option));
   const text=document.createElement('span');text.textContent=option?.textContent||'Đang tải…';
   button.title=option?.textContent||'';button.append(text);
   button.disabled=select.disabled||!select.options.length;
  }
 }
 function normalize(s){return s.normalize('NFD').replace(/[\u0300-\u036f]/g,'').toLowerCase();}
 function render(){
  if(!active)return;
  const {field,select}=active;list.replaceChildren();const term=normalize(search.value);
  for(const option of select.options){
   if(!normalize(option.textContent).includes(term))continue;
   const button=document.createElement('button');button.type='button';button.className='item-picker-option';
   button.setAttribute('role','option');button.setAttribute('aria-selected',String(option.selected));button.title=option.textContent;
   const label=document.createElement('span');label.className='item-picker-item-name';label.textContent=option.textContent;
   button.append(art(field,option),label);
   if(!supplied.has(option.dataset.itemId)){
    const noPhoto=document.createElement('small');noPhoto.className='item-no-image';noPhoto.textContent='Chưa có ảnh';button.append(noPhoto);
   }
   button.addEventListener('click',()=>{
    select.value=option.value;select.dispatchEvent(new Event('change',{bubbles:true}));
    sync();dialog.close();
   });
   list.append(button);
  }
  if(!list.children.length){const p=document.createElement('p');p.className='item-picker-empty';p.textContent='Không tìm thấy trang phục';list.append(p);}
 }
 for(const field of fields){
  const select=document.getElementById(field);if(!select)continue;
  const button=document.createElement('button');button.type='button';button.className='item-picker-button';button.setAttribute('aria-haspopup','dialog');
  const label=document.querySelector('label[for="'+field+'"]');
  button.setAttribute('aria-label','Chọn '+(label?.textContent||field));
  select.parentElement.classList.add('picker-ready');select.parentElement.append(button);pickers.set(field,{select,button});
  button.addEventListener('click',()=>{
   active={field,select,button};title.textContent='Chọn '+label.textContent;search.value='';
   note.textContent=field==='action'?'Hành động chưa có ảnh riêng trong source; ký hiệu dùng để phân biệt.':'Ảnh xem nhanh từ texture gốc; không phải icon trong game.';
   render();dialog.showModal();search.focus();
  });
  new MutationObserver(()=>{sync();if(dialog.open&&active?.field===field)render();}).observe(select,{childList:true,attributes:true,subtree:true});
  select.addEventListener('change',sync);
 }
 search.addEventListener('input',render);
 dialog.querySelector('.item-picker-head button').addEventListener('click',()=>dialog.close());
 dialog.addEventListener('close',()=>active?.button.focus());
 dialog.addEventListener('click',e=>{
  if(e.target===dialog){const r=dialog.getBoundingClientRect();
   if(e.clientX<r.left||e.clientX>r.right||e.clientY<r.top||e.clientY>r.bottom)dialog.close();}
 });
 list.addEventListener('keydown',e=>{
  if(!['ArrowDown','ArrowUp','Home','End'].includes(e.key))return;
  const buttons=[...list.querySelectorAll('button')];if(!buttons.length)return;
  e.preventDefault();const index=buttons.indexOf(document.activeElement);
  buttons[e.key==='Home'?0:e.key==='End'?buttons.length-1:Math.max(0,Math.min(buttons.length-1,index+(e.key==='ArrowDown'?1:-1)))].focus();
 });
 window.addEventListener('wardrobe-change',sync);sync();
})();
