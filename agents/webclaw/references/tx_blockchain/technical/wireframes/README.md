# 🎨 PhoenixPME UI Wireframes & Design System

**Last Updated:** February 24, 2026  
**Status:** ✅ UI Implemented (see `/apps/frontend`)  
**Next:** Wireframes for planned features

---

## 📊 Current Status

| Aspect | Status | Details |
|--------|--------|---------|
| Core UI | ✅ **COMPLETE** | 8 pages implemented, live on Vercel |
| Design System | ✅ **COMPLETE** | Components in `/components/shared/ui/` |
| Mobile Responsive | ✅ **WORKING** | Tested on mobile devices |
| Accessibility | 🟡 **IN PROGRESS** | WCAG 2.1 AA target |
| Wireframes (new features) | 🟢 **PLANNED** | For post-launch features |

---

## ✅ ALREADY IMPLEMENTED COMPONENTS

### Shared UI Components (`/components/shared/ui/`)
| Component | Status | Usage |
|-----------|--------|-------|
| `Button.tsx` | ✅ Complete | Primary, gold, outline variants |
| `FilterTabs.tsx` | ✅ Complete | Metal type filtering |
| `PriceBanner.tsx` | ✅ Complete | Live price display |
| `Toast.tsx` | ✅ Complete | Notification system |

### Layout Components (`/components/layout/`)
| Component | Status | Usage |
|-----------|--------|-------|
| `NavBar.tsx` | ✅ Complete | Navigation with wallet connection |

### Phoenix Branding (`/components/phoenix/`)
| Component | Status | Usage |
|-----------|--------|-------|
| `PhoenixIcon.tsx` | ✅ Complete | Custom SVG logo |
| `Tools.tsx` | ✅ Complete | Developer tools (Excel shortcuts) |

### Auction Components (`/components/auctions/`)
| Component | Status | Usage |
|-----------|--------|-------|
| `AuctionCard.tsx` | ✅ Complete | Individual auction display |
| `AuctionList.tsx` | ✅ Complete | Grid of auctions |
| `BidForm.tsx` | ✅ Complete | Bid placement with collateral |

### Auction Creation Form (`/components/auctions/create/`)
| Component | Status |
|-----------|--------|
| `MetalSelector.tsx` | ✅ Complete |
| `WeightInput.tsx` | ✅ Complete |
| `PuritySelector.tsx` | ✅ Complete |
| `CertificationInput.tsx` | ✅ Complete |
| `SerialNumberInput.tsx` | ✅ Complete |
| `ImageUploader.tsx` | ✅ Complete |
| `FormTypeSelector.tsx` | ✅ Complete |
| `PriceCalculator.tsx` | ✅ Complete |

### Wallet Components
| Component | Status | Usage |
|-----------|--------|-------|
| `UniversalWalletV2.tsx` | ✅ Complete | Multi-wallet (Keplr, Leap, MetaMask, Phantom) |
| `WalletSelector.tsx` | ✅ Complete | Simple wallet selector |
| `TestWalletsPanel.tsx` | ✅ Complete | Sandbox testing |

### Pages Implemented (`/app/`)
| Page | Route | Status |
|------|-------|--------|
| Homepage | `/` | ✅ Complete |
| Auctions Listing | `/auctions` | ✅ Complete |
| Auction Detail | `/auctions/[id]` | ⏳ Planned |
| Create Auction | `/auctions/create` | ✅ Complete |
| Admin Panel | `/admin` | ✅ Complete |
| Sandbox | `/sandbox` | ✅ Complete |
| Not Found | `/_not-found` | ✅ Complete |

---

## 🎨 Design System Guidelines

### Colors
| Color | Usage | Hex |
|-------|-------|-----|
| Primary Amber | Brand primary | `#F59E0B` |
| Dark Amber | Hover states | `#D97706` |
| Deep Amber | Active states | `#B45309` |
| Light Amber | Backgrounds | `#FEF3C7` |
| Gray-50 | Backgrounds | `#F9FAFB` |
| Gray-900 | Text primary | `#111827` |

### Typography
- **Font Family:** Inter (system font stack)
- **Headings:** Bold, large sizes (text-4xl to text-6xl)
- **Body:** text-gray-600, text-gray-900
- **Fine Print:** text-xs text-gray-400

### Spacing
- Consistent `gap-2`, `gap-4`, `mb-12` throughout
- Max-width containers: `max-w-5xl`, `max-w-3xl`
- Padding: `p-4`, `p-6`, `p-8` for cards

### Components
- **Cards:** Rounded-lg, shadow-sm, border-gray-200
- **Buttons:** Rounded-lg, padding, hover effects
- **Forms:** Border-gray-300, focus:ring-amber-500

---

## 📱 Mobile-First Design

All components are designed with mobile-first approach:
- ✅ Responsive grid (grid-cols-1 → md:grid-cols-2)
- ✅ Stack layouts on mobile
- ✅ Touch-friendly tap targets
- ✅ Readable text sizes
- ✅ Collapsible navigation

---

## 🚧 Wireframes Needed (Post-Launch)

| Priority | Wireframe | Status | Notes |
|----------|-----------|--------|-------|
| 🔴 HIGH | Auction Detail Page | ⏳ Planned | Dynamic route `/auctions/[id]` |
| 🔴 HIGH | Settlement Flow | ⏳ Not Started | After delivery confirmation |
| 🟡 MEDIUM | Dispute Resolution UI | ⏳ Not Started | For arbitration |
| 🟡 MEDIUM | User Profile/History | ⏳ Not Started | Trade history, reputation |
| 🟢 LOW | Settings Page | ⏳ Not Started | User preferences |
| 🟢 LOW | Mobile App UI | ⏳ Future | For native apps |

---

## 🛠 Tools & Workflow

### Design Tools
- **Figma** (preferred) - Collaborative design
- **Adobe XD** - Alternative option
- **Pen/paper scans** - Quick ideation
- **Export format**: SVG for icons, PNG for mockups

### File Naming Convention
wireframe_[page-name]_v[version].[extension]
Example: wireframe_auction-detail_v1.fig


### Workflow
1. **Sketch** - Low-fi wireframes
2. **Review** - With team/community
3. **Implement** - Add to codebase
4. **Test** - Responsive, accessibility
5. **Iterate** - Based on feedback

---

## 🔗 Related Documentation

| Document | Link |
|----------|------|
| Architecture Overview | [ARCHITECTURE-OVERVIEW.md](../architecture/ARCHITECTURE-OVERVIEW.md) |
| Current Focus | [CURRENT-FOCUS.md](../CURRENT-FOCUS.md) |
| Roadmap | [ROADMAP.md](../ROADMAP.md) |
| Setup Guide | [SETUP_GUIDE.md](../setup/SETUP_GUIDE.md) |

---

## 📝 Notes

- ✅ **Core UI is already implemented** - No need for wireframes of existing pages
- 🔄 **New features** will require wireframes before implementation
- 🎯 **Design consistency** - All new components should match existing patterns
- ♿ **Accessibility** - Target WCAG 2.1 AA compliance

---

*This document reflects the current state of PhoenixPME UI as of February 24, 2026.*
*Next updates: Wireframes for auction detail page and settlement flow.*