function f = match(f1, d1, frame2, x, y, w, h)
%     tic;
    sz = size(frame2);
%     x 
%     y
%     frame1 = im2single(rgb2gray(frame1));
    frame2 = im2single(rgb2gray(frame2));
%     c1 = [int64(x+(w/2)-35) int64(y+(h/2)-85) int64(x+(w/2)+35) int64(y+(h/2)+85)];
    c1 = [x+(w/2)-35 y+(h/2)-85 x+(w/2)+35 y+(h/2)+85];
    c2 = [max(c1(1)-35,1) max(c1(2)-85,1) min(c1(3)+35,sz(2)) min(c1(4)+85,sz(1))];
    c3 = [c2(1:2) c2(1:2)];
    c4 = c1-c3;
    frame3 = frame2(c2(2):c2(4), c2(1):c2(3));
%     tic;
%     [f1,d1] = vl_sift(frame1);
%     toc;
%     tic;
    [f2,d2] = vl_sift(frame3);
%     toc;
%     sz1 = size(frame1);
%     sz2 = size(frame2);
    sz3 = size(f2);
    d = [];
    f3 = [];
    for i = 1:sz3(2)
%         if f2(1,i) > (x+(w/2)-35) && f2(2,i) > (y+(h/2)-85) && f2(1,i) < (x+(w/2)+35) && f2(2,i) < (y+(h/2)+85)
        if f2(1,i) > c4(1) && f2(2,i) > c4(2) && f2(1,i) < c4(3) && f2(2,i) < c4(4)
            d = [d d2(:,i)];
            f3 = [f3 f2(:,i)];
        end
    end
    [m,s] = vl_ubcmatch(d1,d);
    sz = size(m);
    f4 = [];
    for i = 1:sz(2)
        p = f1(:,m(1,i));
        f4 = [f4 p(1:2)];
    end
    [f5, f6] = sort(f4(1,:));
    f5 = f4(:,f6);
    sz = size(f5);
    f = [];
%     maxcount = 0;
    for i = 1:sz(2)
        count = 0;
        p = f5(:,i);
        j = 1;
        while i+j <= sz(2) & f5(1,i+j) <= p(1)+70
            if f5(2,i+j) >= p(2) & f5(2,i+j) <= p(2)+171
                count = count+1;
            end
            j = j+1;
        end
        f = [f; p' count];
    end
    [a, b] = sort(f(:,3));
    f = f(b,:);
    f = f(end-4:end,:);
%     toc;
%     frame3 = appendimages(frame1,frame2);
%     imshow(frame3);
%     hold on;
%     max(m(1,:));
%     max(m(2,:));
%     for i = 1:sz(2)
%         p1 = f1(:,m(1,i));
%         p2 = f3(:,m(2,i));
%         p1 = p1(1:2);
%         p2 = p2(1:2);
%         p2 = p2 + c2(1:2)';
%         p2(1) = sz1(2)+p2(1);
%         x1 = p1(1);
%         x2 = p2(1);
%         y1 = p1(2);
%         y2 = p2(2);
%         line([x1,x2], [y1,y2]);
%     end
%     hold off;